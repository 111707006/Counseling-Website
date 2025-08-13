#!/bin/bash

# =================================
# Counseling Website 部署腳本
# =================================

set -e  # 遇到錯誤立即退出

# 顏色輸出函數
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

# 檢查必要工具
check_requirements() {
    print_info "檢查系統需求..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安裝。請先安裝 Docker。"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安裝。請先安裝 Docker Compose。"
        exit 1
    fi
    
    print_success "系統需求檢查通過"
}

# 檢查環境變數文件
check_env_file() {
    print_info "檢查環境變數配置..."
    
    if [[ ! -f .env ]]; then
        print_warning ".env 文件不存在，從模板創建..."
        cp .env.example .env
        print_warning "請編輯 .env 文件並填入正確的配置值"
        print_warning "特別注意設置安全的 SECRET_KEY 和資料庫密碼"
        read -p "按 Enter 繼續，或 Ctrl+C 取消部署 "
    fi
    
    print_success "環境變數文件檢查完成"
}

# 構建並啟動服務
deploy_services() {
    local env_file="docker-compose.yml"
    
    if [[ "$1" == "dev" ]]; then
        env_file="docker-compose.dev.yml"
        print_info "啟動開發環境..."
    else
        print_info "啟動生產環境..."
    fi
    
    print_info "停止現有容器..."
    docker-compose -f "$env_file" down
    
    print_info "構建 Docker 鏡像..."
    docker-compose -f "$env_file" build --no-cache
    
    print_info "啟動服務..."
    docker-compose -f "$env_file" up -d
    
    print_info "等待服務啟動..."
    sleep 10
    
    print_info "檢查服務狀態..."
    docker-compose -f "$env_file" ps
}

# 初始化資料庫
init_database() {
    print_info "初始化 Django 資料庫..."
    
    local backend_container="counseling_backend"
    if [[ "$1" == "dev" ]]; then
        backend_container="counseling_backend_dev"
    fi
    
    print_info "等待資料庫就緒..."
    sleep 15
    
    print_info "執行資料庫遷移..."
    docker exec "$backend_container" python manage.py migrate
    
    print_info "收集靜態文件..."
    docker exec "$backend_container" python manage.py collectstatic --noinput
    
    print_info "創建超級管理員帳號（可選）..."
    docker exec -it "$backend_container" python manage.py createsuperuser --noinput || true
    
    print_success "資料庫初始化完成"
}

# 顯示服務狀態
show_status() {
    local env_file="docker-compose.yml"
    if [[ "$1" == "dev" ]]; then
        env_file="docker-compose.dev.yml"
    fi
    
    print_info "服務狀態："
    docker-compose -f "$env_file" ps
    
    print_info "服務日誌（最近 20 行）："
    docker-compose -f "$env_file" logs --tail=20
}

# 主函數
main() {
    local mode="prod"
    local action="deploy"
    
    # 解析命令行參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dev)
                mode="dev"
                shift
                ;;
            --status)
                action="status"
                shift
                ;;
            --init-db)
                action="init-db"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo "選項:"
                echo "  --dev       啟動開發環境"
                echo "  --status    顯示服務狀態"
                echo "  --init-db   初始化資料庫"
                echo "  --help      顯示幫助信息"
                exit 0
                ;;
            *)
                print_error "未知選項: $1"
                echo "使用 --help 查看可用選項"
                exit 1
                ;;
        esac
    done
    
    case $action in
        deploy)
            check_requirements
            check_env_file
            deploy_services "$mode"
            init_database "$mode"
            show_status "$mode"
            
            if [[ "$mode" == "dev" ]]; then
                print_success "開發環境部署完成！"
                print_info "前端: http://localhost:3001"
                print_info "後端 API: http://localhost:8001"
                print_info "資料庫: localhost:3307"
            else
                print_success "生產環境部署完成！"
                print_info "網站: http://localhost"
                print_info "管理後台: http://localhost/admin"
            fi
            ;;
        status)
            show_status "$mode"
            ;;
        init-db)
            init_database "$mode"
            ;;
    esac
}

# 執行主函數
main "$@"
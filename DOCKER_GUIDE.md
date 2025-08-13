# 🐳 Docker 部署指南

## 📋 專案架構

本專案採用微服務架構，包含以下組件：

- **Frontend**: Next.js 18 (React) - 用戶界面
- **Backend**: Django 4.2 + DRF - API 服務
- **Database**: MySQL 8.0 - 資料存儲
- **Proxy**: Nginx - 反向代理和靜態文件服務

## 🔧 Docker 核心原理

### 容器化優勢
- **環境一致性**: 開發、測試、生產環境完全一致
- **資源隔離**: 每個服務運行在獨立容器中
- **可擴展性**: 輕鬆進行水平擴展
- **依賴管理**: 避免"在我機器上可以運行"的問題

### 多階段構建
我們的 Dockerfile 使用多階段構建來優化鏡像大小：

1. **Base Stage**: 安裝依賴和編譯工具
2. **Build Stage**: 構建應用程式
3. **Production Stage**: 僅包含運行時必需文件

## 🚀 快速開始

### 1. 環境準備

**Windows:**
```bash
# 1. 安裝 Docker Desktop
# 2. 確保 WSL2 已啟用
# 3. 複製環境變數文件
copy .env.example .env
```

**Linux/macOS:**
```bash
# 1. 安裝 Docker 和 Docker Compose
# 2. 複製環境變數文件
cp .env.example .env
```

### 2. 配置環境變數

編輯 `.env` 文件，設置以下重要參數：

```env
# 必須更改的安全設定
SECRET_KEY=your-very-secure-secret-key-min-50-chars
MYSQL_ROOT_PASSWORD=very-secure-root-password  
MYSQL_PASSWORD=secure-db-password

# 根據需要調整的配置
ALLOWED_HOSTS=localhost,yourdomain.com
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. 一鍵部署

**Windows 用戶:**
```cmd
# 生產環境
deploy.bat

# 開發環境  
deploy.bat --dev
```

**Linux/macOS 用戶:**
```bash
# 生產環境
./deploy.sh

# 開發環境
./deploy.sh --dev
```

## 🔍 服務詳細配置

### MySQL 資料庫 (Port 3306)
- 自動創建資料庫和用戶
- 使用 UTF8MB4 字符集
- 數據持久化存儲
- 健康檢查機制

### Django 後端 (Port 8000)
```dockerfile
# 多階段構建優化
FROM python:3.11-slim as production
# 非 root 用戶提升安全性
USER django
# Gunicorn 生產服務器
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mindcare.wsgi:application"]
```

### Next.js 前端 (Port 3000)
```dockerfile
# Standalone 模式減少鏡像大小
ENV NEXT_TELEMETRY_DISABLED=1
# 非 root 用戶運行
USER nextjs
CMD ["node", "server.js"]
```

### Nginx 代理 (Port 80)
- 反向代理到前後端服務
- 靜態文件優化服務
- Gzip 壓縮
- 安全標頭設置

## 🎯 環境管理

### 開發環境 (`docker-compose.dev.yml`)
- 代碼熱重載
- 詳細日誌輸出
- 開發用端口 (3001, 8001, 3307)
- 調試模式開啟

### 生產環境 (`docker-compose.yml`)
- 優化的構建配置
- 最小化資源使用
- 安全性配置
- 健康檢查和自動重啟

## 📊 監控和維護

### 查看服務狀態
```bash
# 檢查所有服務
docker-compose ps

# 查看日誌
docker-compose logs -f [service_name]

# 進入容器
docker exec -it counseling_backend bash
```

### 常用維護命令
```bash
# 重新構建服務
docker-compose build --no-cache

# 更新資料庫
docker exec counseling_backend python manage.py migrate

# 收集靜態文件
docker exec counseling_backend python manage.py collectstatic

# 創建管理員帳號
docker exec -it counseling_backend python manage.py createsuperuser
```

## 🔒 安全最佳實踐

### 已實現的安全措施
1. **非 root 用戶**: 所有服務使用專用用戶運行
2. **最小權限原則**: 容器僅包含必需文件
3. **網路隔離**: 服務間通過內部網路通信
4. **環境變數**: 敏感信息通過環境變數傳遞
5. **健康檢查**: 自動檢測服務狀態

### 生產環境建議
1. 使用強密碼和安全的 SECRET_KEY
2. 定期更新 Docker 鏡像
3. 設置 SSL/TLS 證書
4. 配置防火牆規則
5. 定期備份資料庫

## 🐛 常見問題排除

### 服務無法啟動
```bash
# 查看詳細日誌
docker-compose logs [service_name]

# 檢查端口佔用
netstat -tulpn | grep [port]

# 重建容器
docker-compose down && docker-compose up --build
```

### 資料庫連接失敗
1. 確認資料庫容器已啟動
2. 檢查環境變數配置
3. 等待資料庫初始化完成（約 30 秒）

### 前端無法連接後端
1. 確認 `NEXT_PUBLIC_API_BASE_URL` 設置正確
2. 檢查 Django CORS 配置
3. 驗證 Nginx 代理配置

## 📈 性能優化

### Docker 優化建議
1. **多階段構建**: 減少最終鏡像大小
2. **層級緩存**: 合理安排 Dockerfile 指令順序
3. **資源限制**: 設置適當的內存和 CPU 限制
4. **健康檢查**: 及時發現和處理服務異常

### 應用性能優化
1. **靜態文件**: 通過 Nginx 提供，啟用 Gzip
2. **資料庫**: 配置適當的連接池
3. **快取**: 利用 Redis (可選) 進行快取
4. **CDN**: 生產環境建議使用 CDN

## 🔧 自定義配置

### 添加新服務
1. 在 `docker-compose.yml` 中定義新服務
2. 配置網路和依賴關係
3. 更新 Nginx 配置（如需要）

### 擴展功能
- **Redis**: 快取和會話存儲
- **Elasticsearch**: 全文搜索
- **Prometheus**: 監控指標收集
- **Let's Encrypt**: 自動 SSL 證書

## 📞 技術支援

如遇到問題，請檢查：
1. Docker 和 Docker Compose 版本
2. 系統資源是否充足
3. 網路連接是否正常
4. 日誌文件中的錯誤信息

---

**部署成功後的訪問地址：**
- 🌐 網站首頁: http://localhost
- 👨‍💼 管理後台: http://localhost/admin  
- 📱 API 文檔: http://localhost/api/
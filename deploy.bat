@echo off
REM =================================
REM Counseling Website Windows 部署腳本
REM =================================

setlocal enabledelayedexpansion

REM 檢查 Docker
echo [INFO] 檢查 Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker 未安裝或未啟動
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose 未安裝
    pause
    exit /b 1
)

echo [SUCCESS] Docker 檢查通過

REM 檢查環境變數文件
if not exist .env (
    echo [WARNING] .env 文件不存在，從模板創建...
    copy .env.example .env
    echo [WARNING] 請編輯 .env 文件並填入正確的配置值
    pause
)

REM 解析命令行參數
set "MODE=prod"
set "COMPOSE_FILE=docker-compose.yml"

if "%1"=="--dev" (
    set "MODE=dev"
    set "COMPOSE_FILE=docker-compose.dev.yml"
    echo [INFO] 啟動開發環境...
) else (
    echo [INFO] 啟動生產環境...
)

REM 停止並重新構建
echo [INFO] 停止現有容器...
docker-compose -f %COMPOSE_FILE% down

echo [INFO] 構建 Docker 鏡像...
docker-compose -f %COMPOSE_FILE% build --no-cache

echo [INFO] 啟動服務...
docker-compose -f %COMPOSE_FILE% up -d

echo [INFO] 等待服務啟動...
timeout /t 10 >nul

echo [INFO] 檢查服務狀態...
docker-compose -f %COMPOSE_FILE% ps

if "%MODE%"=="dev" (
    echo [SUCCESS] 開發環境部署完成！
    echo [INFO] 前端: http://localhost:3001
    echo [INFO] 後端 API: http://localhost:8001
    echo [INFO] 資料庫: localhost:3307
) else (
    echo [SUCCESS] 生產環境部署完成！
    echo [INFO] 網站: http://localhost
    echo [INFO] 管理後台: http://localhost/admin
)

echo.
echo 是否要初始化資料庫？ (y/n)
set /p init_db=
if /i "%init_db%"=="y" (
    echo [INFO] 初始化資料庫...
    if "%MODE%"=="dev" (
        docker exec counseling_backend_dev python manage.py migrate
        docker exec counseling_backend_dev python manage.py collectstatic --noinput
    ) else (
        docker exec counseling_backend python manage.py migrate
        docker exec counseling_backend python manage.py collectstatic --noinput
    )
    echo [SUCCESS] 資料庫初始化完成
)

pause
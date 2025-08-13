@echo off
chcp 65001 >nul
echo ===============================================
echo      🎉 心理諮詢網站完整啟動腳本
echo ===============================================
echo.

cd /d "%~dp0"

echo [1/4] 檢查 Docker 狀態...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker 未啟動，請先啟動 Docker Desktop
    pause
    exit /b 1
)
echo ✅ Docker 已就緒

echo.
echo [2/4] 停止舊服務...
docker-compose down >nul 2>&1

echo.
echo [3/4] 啟動所有服務...
docker-compose up -d

echo.
echo [4/4] 等待服務啟動...
timeout /t 20 >nul

echo.
echo ===============================================
echo            🚀 網站啟動成功！
echo ===============================================
echo.
echo 📊 服務狀態:
docker-compose ps

echo.
echo 🌐 網站首頁:     http://localhost:3000
echo 📱 前端應用:     http://localhost:3000
echo 🔧 後端 API:     http://localhost:8000
echo 👨‍💼 管理後台:     http://localhost:8000/admin
echo 🗄️ 資料庫:       localhost:3306
echo.
echo 📋 首次使用請執行：
echo docker exec -it counseling_backend python manage.py createsuperuser
echo.
echo 📝 常用指令：
echo 查看日誌： docker-compose logs -f
echo 停止服務： docker-compose down
echo 重啟服務： docker-compose restart
echo.
pause
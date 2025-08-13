@echo off
chcp 65001 >nul
echo ===============================================
echo         簡化版心理諮詢網站啟動腳本
echo ===============================================
echo.

cd /d "%~dp0"

echo [1/3] 檢查 Docker 狀態...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker 未啟動，請先啟動 Docker Desktop
    pause
    exit /b 1
)
echo ✅ Docker 已就緒

echo.
echo [2/3] 啟動資料庫和後端...
docker-compose up db backend -d

echo.
echo [3/3] 等待服務啟動...
timeout /t 15 >nul

echo.
echo ===============================================
echo              基礎服務啟動完成！
echo ===============================================
echo.
echo 📊 服務狀態:
docker-compose ps

echo.
echo 🌐 後端 API:    http://localhost:8000
echo 👨‍💼 管理後台:    http://localhost:8000/admin
echo.
echo 📋 初始化資料庫（首次啟動需要）:
echo docker exec counseling_backend python manage.py migrate
echo docker exec -it counseling_backend python manage.py createsuperuser
echo.
echo 📝 註：前端服務有依賴問題，現在只啟動後端服務
echo      你可以直接訪問 Django 管理界面來管理內容
echo.
pause
# Django Admin 訪問指南

## 🚀 啟動步驟

### 1. 啟動 Django 服務器
```bash
cd "C:\Users\jay\OneDrive\桌面\Counseling Website\backend_temp"
python manage.py runserver 8000
```

### 2. 訪問管理後台
打開瀏覽器訪問：`http://localhost:8000/admin/`

### 3. 登入資訊
- **用戶名**: `admin@mindcare.com`
- **密碼**: `admin123456`

## 📍 在 Admin 中找到 Appointments

登入後，您會看到以下區域：

### APPOINTMENTS 區塊
```
APPOINTMENTS
├── Appointments        ← 這裡！主要的預約管理
├── Appointment details ← 預約詳細資料
└── Preferred periods   ← 偏好時段
```

### THERAPISTS 區塊  
```
THERAPISTS
├── Available times
├── Specialty categories  
├── Specialties
└── Therapist profiles
```

### 其他區塊
```
ARTICLES, ASSESSMENTS, AUTH AND AUTHORIZATION...
```

## 🎯 主要操作位置

1. **點擊 "Appointments"** - 這是主要的預約管理入口
2. 您會看到預約列表，包含：
   - 用戶資訊
   - 心理師分配狀態  
   - 預約狀態
   - 操作按鈕

## 🔧 如果仍然看不到

### 檢查 1: 確認服務器重新啟動
按 `Ctrl+C` 停止服務器，然後重新運行：
```bash
python manage.py runserver 8000
```

### 檢查 2: 清除瀏覽器緩存
- 按 `Ctrl+F5` 強制刷新
- 或清除瀏覽器緩存

### 檢查 3: 確認登入身份
確保使用 `admin@mindcare.com` 登入，而不是其他帳號

## 📊 預約統計 (當前數據)
- 總預約數: 11
- 待處理: 5 (需要您的處理)
- 已確認: 1

## ⚡ 直接訪問 URL
如果在主頁找不到，可以直接訪問：
`http://localhost:8000/admin/appointments/appointment/`

## 🎉 成功標誌
成功進入後，您會看到：
- 預約列表頁面
- 頂部的統計資訊框
- 每筆預約旁邊的操作按鈕 (分配心理師、確認時間、管理狀態)
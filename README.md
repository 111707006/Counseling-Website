
本專案為「心理健康與諮商服務平台」的後端系統，使用 Python Django 與 Django REST Framework 建構。提供多模組 API，包括使用者管理、心理師瀏覽與預約系統、自我心理測驗工具、內容部落格等。

---

## 📌 專案特色

- 採用 Django + DRF 架構，支援 RESTful API
- 使用 JWT 驗證機制，確保使用者身分與資料隱私
- 清楚分工模組化設計（users、appointments、therapists、articles、assessments）
- 可透過 Django Admin 管理所有資料
- 前後端分離架構，適合搭配 Vue、React 或 Next.js

---

## ✅ 功能模組總覽

| 模組 | 說明 |
|------|------|
角色權限管理：支援「一般用戶」、「管理員」身份分流與權限控管。
| 使用者（users） | 註冊、登入（JWT）、個人資訊偏好設定 |
| 心理師（therapists） | 心理師清單瀏覽、專長標籤、收費資訊與線上/實體諮詢選項 |
| 預約（appointments） | 預約心理師，查詢、修改、取消等行為 |管理員可設定可預約時段，並由後台確認與管理。
| 測驗（assessments） | 提供 WHO-5、BSRS-5 測驗，用戶可作答並獲得自我狀態簡析，將來若申請預約可以作為資料 |
| 文章（articles） | 心理健康知識文章，支援分類標籤與作者 |
| 後台（Django Admin） | 可視化後台介面，快速管理心理師、預約與文章內容 |

---

 系統架構
Frontend (React)
│
├── Login / Register
├── Assessment UI (WHO-5, BSRS-5)
├── Article
├── Therapist Profile Pages
└── Admin Dashboard

Backend (Django + DRF)

├── Users (JWT 認證 / 角色權限)
├── Therapists (時段設定 / 回覆留言)
├── Assessments (心理測驗結果分析)
└── Appointments (預約紀錄管理)
└──article(文章增刪查改)

資料庫:資料庫：PostgreSQL
Deployment: Docker
部署:Render 
第三方工具：SendGrid（Email 通知）

模組功能簡述

模組

功能簡介

users/    JWT 登入註冊、用戶身分與權限管理

therapists/   心理師個人簡介、時段設定

appointments/   預約紀錄建立、查詢與取消

assessments/   WHO-5 與 BSRS-5 評量、自動分數計算

admin/    Django 預設後台，用於管理所有資料表


角色         權限描述

一般用戶     可使用聊天、預約、測驗

管理員       可存取 Django admin，編輯所有資料

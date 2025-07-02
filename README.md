# 🧠 MindCare 心理健康平台 – Django REST API 專案說明書

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
| 使用者（users） | 註冊、登入（JWT）、個人資訊偏好設定 |
| 心理師（therapists） | 心理師清單瀏覽、專長標籤、收費資訊與線上/實體諮詢選項 |
| 預約（appointments） | 預約心理師，查詢、修改、取消等行為 |
| 測驗（assessments） | 提供 PHQ-9、GAD-7 等標準心理測驗，計分與自動建議 |
| 文章（articles） | 心理健康知識文章，支援分類標籤與作者 |
| 後台（Django Admin） | 可視化後台介面，快速管理心理師、預約與文章內容 |

---

## 🔐 API 驗證方式：JWT（JSON Web Token）

### 登入取得 Token：

```http
POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}


本專案為「心理健康與諮商服務平台」的後端系統，使用 Python Django 與 Django REST Framework 建構。提供多模組 API，包括使用者管理、心理師瀏覽與預約系統、自我心理測驗工具、內容部落格等。

---

## 📌 專案特色

採用 Django + DRF 架構，支援 RESTful API

採用模組化設計（users、appointments、therapists、articles、assessments）

預約即註冊：簡化用戶操作流程

自我心理測驗整合 WHO-5 / BSRS-5 標準量表

可透過 Django Admin 管理所有資料

前後端分離架構，適合搭配 React / Vue / Next.js

使用 PostgreSQL 資料庫、Docker 容器化部署（支援 Render）

整合 SendGrid 寄送預約通知信件
---

## ✅ 功能模組總覽

使用者（users）	✨ 無需傳統註冊登入流程。用戶填寫預約表單即自動註冊，後續以 Email + 身分證字號查詢預約紀錄

心理師（therapists）	心理師清單瀏覽、個人簡介、專長標籤、線上/實體選項與收費設定，由管理員維護

預約（appointments）	用戶可預約心理師，選擇諮詢方式(實體/線上)。管理員後台可查詢並確認／取消

測驗（assessments）	提供 WHO-5 與 BSRS-5 測驗，自動計分與分級，若風險高則建立臨時資料庫，可供預約時參考

文章（articles）	心理健康相關文章，支援分類與標籤，可由管理員建立與編輯

後台（Django Admin）	可視化後台介面，管理心理師、預約、測驗結果與文章內容
---

 系統架構
Frontend (React)


├── 首頁（介紹／導引）
├── Assessment 測驗頁面（WHO-5、BSRS-5）
├── Therapist 心理師介紹頁(諮商室介紹)
├── Article(文章)
├── 預約表單（即時註冊）
├── 預約查詢／取消（Email + 身分證登入）
└── 管理員登入／Django Admin（僅後台）


Backend (Django + DRF)

├── Users 使用者建立、身分驗證、查詢身分
├── Therapists 心理師簡介/可供心理師修改自介
├── Assessments (心理測驗結果分析)
└── Appointments 預約表單、狀態變更、查詢與取消
└──article(文章增刪查改)
└──admin/ 後台管理界面


資料庫:資料庫：PostgreSQL
Deployment: Docker
部署:Render 
第三方工具：SendGrid（Email 通知）

模組功能簡述

模組


角色         權限描述

一般用戶     可使用預約、測驗、檢視文章

管理員       可存取 Django admin，編輯所有資料

心理師       可幫用戶預約諮商，查看個案資訊、行程表，薪資表

## 🔐 身分驗證機制：預約即註冊、Email + 身分證查詢

本系統已移除傳統註冊／登入流程，改採「預約即註冊」設計，降低使用者進入門檻。

1. 用戶在預約表單填寫：
   - 姓名（前端可額外收集，後端會記錄）
   - **Email**（作為唯一帳號識別）
   - **身分證字號**（後端雜湊儲存，不以明文保存）
   - 選擇心理師、時段、諮詢方式

2. 系統自動：
   - 若 Email 尚未註冊 → 建立新 User 並雜湊儲存身分證
   - 建立預約紀錄（狀態 `pending`）

3. 未來查詢／取消預約：
   - 進入「預約查詢」頁面
   - 提供 **Email + 身分證字號** 即可驗證身份
   - 列出該用戶所有預約紀錄，並可取消未確認的預約

心理師	管理員後台建立	獨立後台登入（JWT）	可查看自己時段、預約紀錄、個案測驗資料、行程表與薪資
管理員	超級使用者或直接建	Django Admin 或 JWT	可操作所有資料，包含建立心理師、查詢預約

此機制：
- 保留 Django `username` 欄位於後端作為內部識別，前端不顯示
- 心理師／管理員登入仍使用 JWT（原有 token API 留作後台使用）


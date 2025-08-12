# 網站訪客統計系統

這是一個完整的網站訪客統計分析系統，可以追蹤和分析網站的訪客行為。

## 功能特色

### 🔍 數據追蹤
- **訪客會話追蹤**: IP地址、設備類型、瀏覽器、操作系統
- **頁面瀏覽記錄**: 頁面路徑、停留時間、滾動深度
- **來源分析**: 推薦來源、UTM參數追蹤
- **實時心跳**: 30秒間隔的活動追蹤

### 📊 統計分析
- **每日統計**: 獨立訪客、頁面瀏覽數、會話時長
- **熱門頁面**: 最受歡迎的頁面排行
- **設備統計**: 手機、平板、桌機使用比例
- **瀏覽器統計**: 不同瀏覽器的使用情況

### 🎛️ 管理後台
- **Django Admin 集成**: 完整的後台管理界面
- **可視化儀表板**: 圖表和統計卡片
- **數據導出**: 支援CSV等格式導出
- **權限控制**: 僅管理員可查看統計

## 安裝步驟

### 1. 後端設置

```bash
# 1. 安裝依賴
pip install user-agents

# 2. 應用數據庫遷移
python manage.py migrate analytics

# 3. 重新啟動Django服務器
python manage.py runserver
```

### 2. 前端集成

在您的Next.js項目中，將分析代碼集成到主要布局或組件中：

```typescript
// 在 layout.tsx 或 _app.tsx 中
import { useAnalytics } from '@/hooks/useAnalytics';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // 自動啟動分析追蹤
  useAnalytics();

  return (
    <html lang="zh-TW">
      <body>
        {children}
      </body>
    </html>
  );
}
```

或者直接導入分析庫：

```typescript
import analytics from '@/lib/analytics';

// 手動追蹤事件
analytics?.trackCustomEvent('button_click', {
  button_name: '預約諮詢',
  page_path: window.location.pathname
});
```

## 使用方法

### 查看統計數據

1. **Django Admin**: 
   - 登入管理後台 `/admin/`
   - 查看 "Analytics" 區塊中的各項數據

2. **分析儀表板**:
   - 訪問 `/admin/` 後點擊相應鏈接
   - 或直接訪問 `/analytics/dashboard/`

### API 端點

系統提供以下API端點：

- `POST /analytics/api/track-visit/` - 追蹤頁面訪問
- `POST /analytics/api/track-event/` - 追蹤自定義事件  
- `GET /analytics/api/stats/` - 獲取基本統計數據

### 自定義事件追蹤

```javascript
// 追蹤按鈕點擊
analytics.trackCustomEvent('button_click', {
  button_text: '立即預約',
  section: 'hero'
});

// 追蹤表單提交
analytics.trackCustomEvent('form_submit', {
  form_name: 'contact_form',
  success: true
});

// 追蹤文章閱讀
analytics.trackCustomEvent('article_read', {
  article_id: 123,
  reading_time: 180 // 秒
});
```

## 數據模型

### VisitorSession (訪客會話)
- 會話ID、IP地址、用戶代理
- 設備類型、瀏覽器、操作系統  
- 地理位置、來源信息
- 會話統計（頁面數、持續時間）

### PageView (頁面瀏覽)
- 關聯會話、頁面路徑、頁面標題
- 訪問時間、停留時間、滾動深度
- 跳出分析

### DailyStats (每日統計)
- 獨立訪客數、總頁面瀏覽數
- 平均會話時長、跳出率
- 新舊用戶比例

### PopularPage (熱門頁面)
- 頁面路徑、總瀏覽次數
- 獨立瀏覽次數、平均停留時間

## 隱私與合規

### 數據收集原則
- **匿名收集**: 不收集個人身份信息
- **透明度**: 可選擇提供隱私政策說明
- **用戶控制**: 支援禁用追蹤功能

### 禁用追蹤
```javascript
// 禁用追蹤
analytics.setTrackingEnabled(false);

// 或在本地存儲中設置
localStorage.setItem('analytics_disabled', 'true');
```

## 性能考量

- **異步追蹤**: 所有追蹤請求都是異步執行，不影響頁面性能
- **失敗容錯**: 網絡錯誤時靜默失敗，不干擾用戶體驗
- **批量發送**: 使用 sendBeacon API 確保數據在頁面關閉時能被發送
- **數據清理**: 建議定期清理舊數據以維持性能

## 故障排除

### 常見問題

1. **數據沒有被追蹤**
   - 檢查瀏覽器控制台是否有錯誤
   - 確認API端點可以正常訪問
   - 檢查CORS設置

2. **統計數據不準確**
   - 確認時區設置正確
   - 檢查是否有重複的會話ID
   - 驗證數據庫中的時間戳

3. **性能問題**
   - 檢查數據庫索引是否建立
   - 考慮定期清理舊數據
   - 監控API響應時間

### 調試模式

在開發環境中啟用調試：

```javascript
// 檢查追蹤狀態
console.log('Session ID:', analytics.getSessionId());
console.log('Tracking enabled:', analytics.trackingEnabled);

// 手動獲取統計數據
analytics.getStats().then(stats => {
  console.log('Website stats:', stats);
});
```

## 未來增強

可能的功能擴展：

- **地理位置分析**: 集成IP地理定位服務
- **A/B測試支援**: 添加實驗追蹤功能
- **實時儀表板**: WebSocket實時數據更新
- **數據導出**: 更多格式的數據導出選項
- **告警系統**: 異常流量或錯誤告警

## 聯繫支援

如有技術問題或功能建議，請聯繫開發團隊。

---

**注意**: 請確保遵循當地的數據保護法規，如GDPR、CCPA等，在收集用戶數據時提供適當的通知和選擇機制。
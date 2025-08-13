import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import analytics from '@/lib/analytics';

/**
 * 網站分析 Hook
 * 自動追蹤頁面瀏覽和路由變化
 */
export function useAnalytics() {
  const pathname = usePathname();

  useEffect(() => {
    // 當路由變化時，追蹤新的頁面瀏覽
    if (analytics && typeof window !== 'undefined') {
      // 重置頁面開始時間和滾動深度
      (analytics as any).pageStartTime = Date.now();
      (analytics as any).maxScrollDepth = 0;
      
      // 追蹤新頁面
      const trackData = {
        session_id: analytics.getSessionId(),
        page_path: pathname,
        page_title: document.title,
        referrer: document.referrer,
        timestamp: new Date().toISOString(),
      };

      (analytics as any).sendTrackingData('/api/track-visit/', trackData);
    }
  }, [pathname]);

  // 返回分析實例和便利方法
  return {
    analytics,
    trackEvent: (eventName: string, eventData?: any) => {
      if (analytics) {
        analytics.trackCustomEvent(eventName, eventData);
      }
    },
    getSessionId: () => {
      return analytics?.getSessionId() || null;
    },
    setTrackingEnabled: (enabled: boolean) => {
      if (analytics) {
        analytics.setTrackingEnabled(enabled);
      }
    },
  };
}
// 網站分析追蹤工具
class WebsiteAnalytics {
  private sessionId: string;
  private apiBase: string;
  private pageStartTime: number;
  private maxScrollDepth: number;
  private trackingEnabled: boolean;

  constructor() {
    this.sessionId = this.getOrCreateSessionId();
    this.apiBase = process.env.NODE_ENV === 'production' 
      ? 'https://your-domain.com/analytics' 
      : 'http://localhost:8000/analytics';
    this.pageStartTime = Date.now();
    this.maxScrollDepth = 0;
    this.trackingEnabled = true;
    
    this.initializeTracking();
  }

  /**
   * 獲取或創建會話ID
   */
  private getOrCreateSessionId(): string {
    let sessionId = sessionStorage.getItem('website_analytics_session_id');
    if (!sessionId) {
      sessionId = this.generateUUID();
      sessionStorage.setItem('website_analytics_session_id', sessionId);
    }
    return sessionId;
  }

  /**
   * 生成UUID
   */
  private generateUUID(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  /**
   * 初始化追蹤功能
   */
  private initializeTracking(): void {
    if (!this.trackingEnabled) return;

    // 追蹤頁面瀏覽
    this.trackPageView();

    // 追蹤滾動深度
    this.trackScrollDepth();

    // 追蹤頁面離開
    this.trackPageLeave();

    // 定期發送心跳
    this.startHeartbeat();
  }

  /**
   * 追蹤頁面瀏覽
   */
  private trackPageView(): void {
    const data = {
      session_id: this.sessionId,
      page_path: window.location.pathname,
      page_title: document.title,
      referrer: document.referrer,
      user_agent: navigator.userAgent,
      screen_resolution: `${screen.width}x${screen.height}`,
      viewport_size: `${window.innerWidth}x${window.innerHeight}`,
      timestamp: new Date().toISOString(),
      // UTM 參數
      utm_source: this.getUrlParameter('utm_source'),
      utm_medium: this.getUrlParameter('utm_medium'),
      utm_campaign: this.getUrlParameter('utm_campaign'),
    };

    this.sendTrackingData('/api/track-visit/', data);
  }

  /**
   * 追蹤滾動深度
   */
  private trackScrollDepth(): void {
    let ticking = false;

    const updateScrollDepth = () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollDepth = Math.round((scrollTop / documentHeight) * 100);

      if (scrollDepth > this.maxScrollDepth) {
        this.maxScrollDepth = Math.min(scrollDepth, 100);
      }
      ticking = false;
    };

    const onScroll = () => {
      if (!ticking) {
        requestAnimationFrame(updateScrollDepth);
        ticking = true;
      }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /**
   * 追蹤頁面離開
   */
  private trackPageLeave(): void {
    const trackLeave = () => {
      const timeOnPage = Math.round((Date.now() - this.pageStartTime) / 1000);
      
      const data = {
        session_id: this.sessionId,
        page_path: window.location.pathname,
        time_on_page: timeOnPage,
        scroll_depth: this.maxScrollDepth,
        timestamp: new Date().toISOString(),
      };

      // 使用 sendBeacon 確保數據在頁面離開時能被發送
      this.sendBeaconData('/api/track-event/', data);
    };

    // 多種離開事件
    window.addEventListener('beforeunload', trackLeave);
    window.addEventListener('pagehide', trackLeave);
    
    // 對於單頁應用，監聽路由變化
    window.addEventListener('popstate', trackLeave);
  }

  /**
   * 開始心跳追蹤
   */
  private startHeartbeat(): void {
    // 每30秒發送一次心跳
    setInterval(() => {
      const timeOnPage = Math.round((Date.now() - this.pageStartTime) / 1000);
      
      const data = {
        session_id: this.sessionId,
        page_path: window.location.pathname,
        time_on_page: timeOnPage,
        scroll_depth: this.maxScrollDepth,
        timestamp: new Date().toISOString(),
      };

      this.sendTrackingData('/api/track-event/', data);
    }, 30000); // 30秒
  }

  /**
   * 發送追蹤數據
   */
  private async sendTrackingData(endpoint: string, data: any): Promise<void> {
    try {
      const response = await fetch(this.apiBase + endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        console.warn('Analytics tracking failed:', response.status);
      }
    } catch (error) {
      console.warn('Analytics tracking error:', error);
    }
  }

  /**
   * 使用 sendBeacon 發送數據
   */
  private sendBeaconData(endpoint: string, data: any): void {
    try {
      const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
      
      if (navigator.sendBeacon) {
        navigator.sendBeacon(this.apiBase + endpoint, blob);
      } else {
        // Fallback for browsers that don't support sendBeacon
        this.sendTrackingData(endpoint, data);
      }
    } catch (error) {
      console.warn('Analytics beacon error:', error);
    }
  }

  /**
   * 獲取URL參數
   */
  private getUrlParameter(name: string): string {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name) || '';
  }

  /**
   * 手動追蹤自定義事件
   */
  public trackCustomEvent(eventName: string, eventData: any = {}): void {
    if (!this.trackingEnabled) return;

    const data = {
      session_id: this.sessionId,
      page_path: window.location.pathname,
      event_name: eventName,
      event_data: eventData,
      timestamp: new Date().toISOString(),
    };

    this.sendTrackingData('/api/track-event/', data);
  }

  /**
   * 啟用/禁用追蹤
   */
  public setTrackingEnabled(enabled: boolean): void {
    this.trackingEnabled = enabled;
    if (enabled) {
      console.log('Website analytics tracking enabled');
    } else {
      console.log('Website analytics tracking disabled');
    }
  }

  /**
   * 獲取當前會話ID
   */
  public getSessionId(): string {
    return this.sessionId;
  }

  /**
   * 獲取統計數據 (僅供管理員使用)
   */
  public async getStats(): Promise<any> {
    try {
      const response = await fetch(this.apiBase + '/api/stats/');
      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Failed to get analytics stats:', error);
    }
    return null;
  }
}

// 自動初始化 (如果在瀏覽器環境中)
let analytics: WebsiteAnalytics | null = null;

if (typeof window !== 'undefined') {
  analytics = new WebsiteAnalytics();
  
  // 將實例掛載到全局對象上，方便調試和手動追蹤
  (window as any).analytics = analytics;
}

export default analytics;
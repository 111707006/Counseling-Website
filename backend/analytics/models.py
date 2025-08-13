from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class VisitorSession(models.Model):
    """訪客會話記錄"""
    session_id = models.CharField(max_length=255, unique=True, help_text="會話ID")
    ip_address = models.GenericIPAddressField(help_text="訪客IP地址")
    user_agent = models.TextField(blank=True, help_text="瀏覽器用戶代理")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, help_text="關聯用戶(如已登入)")
    
    # 訪客地理信息
    country = models.CharField(max_length=100, blank=True, help_text="國家")
    city = models.CharField(max_length=100, blank=True, help_text="城市")
    
    # 設備信息
    device_type = models.CharField(max_length=50, blank=True, help_text="設備類型(mobile/desktop/tablet)")
    browser = models.CharField(max_length=100, blank=True, help_text="瀏覽器")
    os = models.CharField(max_length=100, blank=True, help_text="操作系統")
    
    # 時間記錄
    first_visit = models.DateTimeField(default=timezone.now, help_text="首次訪問時間")
    last_activity = models.DateTimeField(default=timezone.now, help_text="最後活動時間")
    
    # 會話統計
    page_views = models.PositiveIntegerField(default=0, help_text="頁面瀏覽數")
    session_duration = models.DurationField(null=True, blank=True, help_text="會話持續時間")
    
    # 來源信息
    referrer = models.URLField(blank=True, help_text="來源網址")
    utm_source = models.CharField(max_length=255, blank=True, help_text="UTM來源")
    utm_medium = models.CharField(max_length=255, blank=True, help_text="UTM媒介")
    utm_campaign = models.CharField(max_length=255, blank=True, help_text="UTM活動")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_activity']
        verbose_name = "訪客會話"
        verbose_name_plural = "訪客會話"

    def __str__(self):
        return f"{self.ip_address} - {self.first_visit.strftime('%Y-%m-%d %H:%M')}"

    def update_activity(self):
        """更新最後活動時間和會話持續時間"""
        now = timezone.now()
        self.last_activity = now
        self.session_duration = now - self.first_visit
        self.save(update_fields=['last_activity', 'session_duration'])


class PageView(models.Model):
    """頁面瀏覽記錄"""
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='pageviews', help_text="關聯會話")
    
    # 頁面信息
    page_path = models.CharField(max_length=500, help_text="頁面路徑")
    page_title = models.CharField(max_length=255, blank=True, help_text="頁面標題")
    page_category = models.CharField(max_length=100, blank=True, help_text="頁面分類")
    
    # 訪問詳情
    visit_time = models.DateTimeField(default=timezone.now, help_text="訪問時間")
    time_on_page = models.PositiveIntegerField(null=True, blank=True, help_text="頁面停留時間(秒)")
    
    # 用戶行為
    scroll_depth = models.PositiveIntegerField(null=True, blank=True, help_text="滾動深度百分比")
    is_bounce = models.BooleanField(default=True, help_text="是否跳出")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_time']
        verbose_name = "頁面瀏覽"
        verbose_name_plural = "頁面瀏覽"

    def __str__(self):
        return f"{self.page_path} - {self.visit_time.strftime('%Y-%m-%d %H:%M')}"

    @classmethod
    def get_popular_pages(cls, days=30):
        """獲取熱門頁面"""
        from django.utils import timezone
        from django.db.models import Count
        
        start_date = timezone.now() - timezone.timedelta(days=days)
        return cls.objects.filter(visit_time__gte=start_date)\
                         .values('page_path', 'page_title')\
                         .annotate(views=Count('id'))\
                         .order_by('-views')[:10]


class DailyStats(models.Model):
    """每日統計數據"""
    date = models.DateField(unique=True, help_text="日期")
    
    # 基本統計
    unique_visitors = models.PositiveIntegerField(default=0, help_text="獨立訪客數")
    total_pageviews = models.PositiveIntegerField(default=0, help_text="總頁面瀏覽數")
    total_sessions = models.PositiveIntegerField(default=0, help_text="總會話數")
    
    # 用戶行為統計
    avg_session_duration = models.DurationField(null=True, blank=True, help_text="平均會話時長")
    avg_pages_per_session = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="每會話平均頁面數")
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="跳出率")
    
    # 新舊用戶統計
    new_visitors = models.PositiveIntegerField(default=0, help_text="新訪客數")
    returning_visitors = models.PositiveIntegerField(default=0, help_text="回訪用戶數")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "每日統計"
        verbose_name_plural = "每日統計"

    def __str__(self):
        return f"{self.date} - {self.unique_visitors} 訪客"

    @classmethod
    def generate_daily_stats(cls, date=None):
        """生成指定日期的統計數據"""
        if date is None:
            date = timezone.now().date()
        
        # 獲取當天的數據
        sessions = VisitorSession.objects.filter(first_visit__date=date)
        pageviews = PageView.objects.filter(visit_time__date=date)
        
        # 計算統計數據
        unique_visitors = sessions.count()
        total_pageviews = pageviews.count()
        total_sessions = sessions.count()
        
        # 更新或創建統計記錄
        stats, created = cls.objects.get_or_create(
            date=date,
            defaults={
                'unique_visitors': unique_visitors,
                'total_pageviews': total_pageviews,
                'total_sessions': total_sessions,
            }
        )
        
        if not created:
            stats.unique_visitors = unique_visitors
            stats.total_pageviews = total_pageviews
            stats.total_sessions = total_sessions
            stats.save()
        
        return stats


class PopularPage(models.Model):
    """熱門頁面統計"""
    page_path = models.CharField(max_length=500, help_text="頁面路徑")
    page_title = models.CharField(max_length=255, blank=True, help_text="頁面標題")
    page_category = models.CharField(max_length=100, blank=True, help_text="頁面分類")
    
    # 統計數據
    total_views = models.PositiveIntegerField(default=0, help_text="總瀏覽次數")
    unique_views = models.PositiveIntegerField(default=0, help_text="獨立瀏覽次數")
    avg_time_on_page = models.PositiveIntegerField(null=True, blank=True, help_text="平均停留時間(秒)")
    
    # 時間範圍
    last_updated = models.DateTimeField(auto_now=True, help_text="最後更新時間")

    class Meta:
        ordering = ['-total_views']
        verbose_name = "熱門頁面"
        verbose_name_plural = "熱門頁面"

    def __str__(self):
        return f"{self.page_title or self.page_path} - {self.total_views} 次瀏覽"

    @classmethod
    def update_popular_pages(cls):
        """更新熱門頁面統計"""
        from django.db.models import Count, Avg
        
        # 獲取過去30天的數據
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        
        popular_data = PageView.objects.filter(visit_time__gte=thirty_days_ago)\
                                     .values('page_path', 'page_title', 'page_category')\
                                     .annotate(
                                         total_views=Count('id'),
                                         unique_views=Count('session', distinct=True),
                                         avg_time=Avg('time_on_page')
                                     )\
                                     .order_by('-total_views')
        
        # 清除舊數據並插入新數據
        cls.objects.all().delete()
        
        for data in popular_data:
            cls.objects.create(
                page_path=data['page_path'],
                page_title=data['page_title'] or '',
                page_category=data['page_category'] or '',
                total_views=data['total_views'],
                unique_views=data['unique_views'],
                avg_time_on_page=data['avg_time'] or 0
            )

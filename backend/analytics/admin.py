from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta

from .models import VisitorSession, PageView, DailyStats, PopularPage


class PageViewInline(admin.TabularInline):
    """頁面瀏覽記錄的內嵌管理"""
    model = PageView
    extra = 0
    readonly_fields = ('page_path', 'page_title', 'visit_time', 'time_on_page', 'scroll_depth')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    """訪客會話管理"""
    list_display = (
        'id', 'ip_address', 'get_user_display', 'device_type', 
        'browser', 'page_views', 'get_duration', 'first_visit'
    )
    
    list_filter = (
        'device_type', 'browser', 'os', 'country', 'first_visit'
    )
    
    search_fields = (
        'ip_address', 'user__email', 'user_agent', 'session_id'
    )
    
    readonly_fields = (
        'session_id', 'ip_address', 'user_agent', 'user',
        'first_visit', 'last_activity', 'session_duration', 'page_views'
    )
    
    inlines = [PageViewInline]
    
    ordering = ('-first_visit',)
    
    def get_user_display(self, obj):
        if obj.user:
            return obj.user.email
        return "匿名用戶"
    get_user_display.short_description = "用戶"
    
    def get_duration(self, obj):
        if obj.session_duration:
            total_seconds = int(obj.session_duration.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}分{seconds}秒"
        return "未知"
    get_duration.short_description = "會話時長"
    
    def has_add_permission(self, request):
        return False


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    """頁面瀏覽管理"""
    list_display = (
        'id', 'page_path', 'page_title', 'get_session_ip', 
        'visit_time', 'get_time_on_page', 'scroll_depth'
    )
    
    list_filter = (
        'page_category', 'is_bounce', 'visit_time'
    )
    
    search_fields = (
        'page_path', 'page_title', 'session__ip_address'
    )
    
    readonly_fields = (
        'session', 'page_path', 'page_title', 'visit_time', 
        'time_on_page', 'scroll_depth', 'is_bounce'
    )
    
    ordering = ('-visit_time',)
    
    def get_session_ip(self, obj):
        return obj.session.ip_address
    get_session_ip.short_description = "訪客IP"
    
    def get_time_on_page(self, obj):
        if obj.time_on_page:
            return f"{obj.time_on_page} 秒"
        return "未知"
    get_time_on_page.short_description = "停留時間"
    
    def has_add_permission(self, request):
        return False


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    """每日統計管理"""
    list_display = (
        'date', 'unique_visitors', 'total_pageviews', 'total_sessions',
        'get_avg_duration', 'avg_pages_per_session', 'get_bounce_rate'
    )
    
    list_filter = ('date',)
    
    readonly_fields = (
        'date', 'unique_visitors', 'total_pageviews', 'total_sessions',
        'avg_session_duration', 'avg_pages_per_session', 'bounce_rate',
        'new_visitors', 'returning_visitors'
    )
    
    ordering = ('-date',)
    
    def get_avg_duration(self, obj):
        if obj.avg_session_duration:
            total_seconds = int(obj.avg_session_duration.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}分{seconds}秒"
        return "未知"
    get_avg_duration.short_description = "平均時長"
    
    def get_bounce_rate(self, obj):
        if obj.bounce_rate:
            return f"{obj.bounce_rate}%"
        return "未知"
    get_bounce_rate.short_description = "跳出率"
    
    def has_add_permission(self, request):
        return False


@admin.register(PopularPage)
class PopularPageAdmin(admin.ModelAdmin):
    """熱門頁面管理"""
    list_display = (
        'page_title', 'page_path', 'page_category',
        'total_views', 'unique_views', 'get_avg_time', 'last_updated'
    )
    
    list_filter = ('page_category', 'last_updated')
    
    search_fields = ('page_path', 'page_title')
    
    readonly_fields = (
        'page_path', 'page_title', 'page_category',
        'total_views', 'unique_views', 'avg_time_on_page', 'last_updated'
    )
    
    ordering = ('-total_views',)
    
    def get_avg_time(self, obj):
        if obj.avg_time_on_page:
            return f"{obj.avg_time_on_page} 秒"
        return "未知"
    get_avg_time.short_description = "平均停留時間"
    
    def has_add_permission(self, request):
        return False


class AnalyticsAdminSite(admin.AdminSite):
    """自定義的分析後台"""
    site_header = "網站流量分析"
    site_title = "分析後台"
    index_title = "網站統計儀表板"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics-dashboard/', self.dashboard_view, name='analytics_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """統計儀表板視圖"""
        # 獲取基本統計數據
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        seven_days_ago = today - timedelta(days=7)
        
        # 總體統計
        total_visitors = VisitorSession.objects.count()
        total_pageviews = PageView.objects.count()
        
        # 最近30天統計
        recent_visitors = VisitorSession.objects.filter(
            first_visit__date__gte=thirty_days_ago
        ).count()
        recent_pageviews = PageView.objects.filter(
            visit_time__date__gte=thirty_days_ago
        ).count()
        
        # 今日統計
        today_visitors = VisitorSession.objects.filter(
            first_visit__date=today
        ).count()
        today_pageviews = PageView.objects.filter(
            visit_time__date=today
        ).count()
        
        # 熱門頁面（最近30天）
        popular_pages = PageView.objects.filter(
            visit_time__date__gte=thirty_days_ago
        ).values('page_path', 'page_title').annotate(
            views=Count('id')
        ).order_by('-views')[:10]
        
        # 每日訪客趨勢（最近7天）
        daily_trends = []
        for i in range(7):
            date = today - timedelta(days=6-i)
            visitors = VisitorSession.objects.filter(
                first_visit__date=date
            ).count()
            pageviews = PageView.objects.filter(
                visit_time__date=date
            ).count()
            daily_trends.append({
                'date': date,
                'visitors': visitors,
                'pageviews': pageviews
            })
        
        # 設備統計
        device_stats = VisitorSession.objects.filter(
            first_visit__date__gte=thirty_days_ago
        ).values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # 瀏覽器統計
        browser_stats = VisitorSession.objects.filter(
            first_visit__date__gte=thirty_days_ago
        ).values('browser').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        context = {
            'title': '網站分析儀表板',
            'total_visitors': total_visitors,
            'total_pageviews': total_pageviews,
            'recent_visitors': recent_visitors,
            'recent_pageviews': recent_pageviews,
            'today_visitors': today_visitors,
            'today_pageviews': today_pageviews,
            'popular_pages': popular_pages,
            'daily_trends': daily_trends,
            'device_stats': device_stats,
            'browser_stats': browser_stats,
        }
        
        return render(request, 'admin/analytics/dashboard.html', context)


# 如果要覆蓋默認的admin站點，可以取消註釋以下行
# admin.site = AnalyticsAdminSite()

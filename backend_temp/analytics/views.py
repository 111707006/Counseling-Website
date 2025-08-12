from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg, Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
import uuid
import re
from user_agents import parse

from .models import VisitorSession, PageView, DailyStats, PopularPage


def get_client_ip(request):
    """獲取客戶端真實IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_user_agent(user_agent_string):
    """解析用戶代理字符串"""
    user_agent = parse(user_agent_string)
    
    # 設備類型
    if user_agent.is_mobile:
        device_type = 'mobile'
    elif user_agent.is_tablet:
        device_type = 'tablet'
    else:
        device_type = 'desktop'
    
    # 瀏覽器和操作系統
    browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
    os = f"{user_agent.os.family} {user_agent.os.version_string}"
    
    return device_type, browser, os


def categorize_page(page_path):
    """根據頁面路徑分類頁面"""
    if page_path == '/':
        return '首頁'
    elif page_path.startswith('/articles'):
        return '心理健康文章'
    elif page_path.startswith('/appointments'):
        return '預約諮詢'
    elif page_path.startswith('/therapists'):
        return '心理師介紹'
    elif page_path.startswith('/assessments'):
        return '心理測驗'
    elif page_path.startswith('/announcements'):
        return '最新消息'
    else:
        return '其他'


@api_view(['POST'])
@permission_classes([AllowAny])
def track_visit(request):
    """追蹤訪客訪問"""
    try:
        data = request.data
        
        # 獲取或創建會話
        session_id = data.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # 獲取客戶端信息
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # 解析用戶代理
        device_type, browser, os = parse_user_agent(user_agent)
        
        # 獲取或創建訪客會話
        session, created = VisitorSession.objects.get_or_create(
            session_id=session_id,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'device_type': device_type,
                'browser': browser,
                'os': os,
                'referrer': data.get('referrer', ''),
                'utm_source': data.get('utm_source', ''),
                'utm_medium': data.get('utm_medium', ''),
                'utm_campaign': data.get('utm_campaign', ''),
            }
        )
        
        # 更新會話活動
        if not created:
            session.update_activity()
        
        # 記錄頁面瀏覽
        page_path = data.get('page_path', '/')
        page_title = data.get('page_title', '')
        page_category = categorize_page(page_path)
        
        page_view = PageView.objects.create(
            session=session,
            page_path=page_path,
            page_title=page_title,
            page_category=page_category,
            time_on_page=data.get('time_on_page'),
            scroll_depth=data.get('scroll_depth'),
        )
        
        # 更新會話的頁面瀏覽數
        session.page_views = session.pageviews.count()
        session.save(update_fields=['page_views'])
        
        # 如果這不是會話的第一個頁面，將前一個頁面的跳出狀態設為False
        if session.pageviews.count() > 1:
            previous_views = session.pageviews.exclude(id=page_view.id)
            previous_views.update(is_bounce=False)
        
        return Response({
            'success': True,
            'session_id': session_id,
            'message': 'Visit tracked successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def track_event(request):
    """追蹤特定事件"""
    try:
        data = request.data
        session_id = data.get('session_id')
        
        if not session_id:
            return Response({
                'success': False,
                'error': 'Session ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session = VisitorSession.objects.get(session_id=session_id)
            session.update_activity()
        except VisitorSession.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Session not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 更新頁面停留時間和滾動深度
        current_page = data.get('page_path', '/')
        time_on_page = data.get('time_on_page')
        scroll_depth = data.get('scroll_depth')
        
        if time_on_page is not None or scroll_depth is not None:
            page_views = session.pageviews.filter(page_path=current_page).order_by('-visit_time')
            if page_views.exists():
                latest_view = page_views.first()
                if time_on_page is not None:
                    latest_view.time_on_page = time_on_page
                if scroll_depth is not None:
                    latest_view.scroll_depth = scroll_depth
                latest_view.save()
        
        return Response({
            'success': True,
            'message': 'Event tracked successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stats(request):
    """獲取統計數據"""
    try:
        # 基本統計
        total_visitors = VisitorSession.objects.count()
        total_pageviews = PageView.objects.count()
        
        # 今日統計
        today = timezone.now().date()
        today_visitors = VisitorSession.objects.filter(
            first_visit__date=today
        ).count()
        today_pageviews = PageView.objects.filter(
            visit_time__date=today
        ).count()
        
        # 熱門頁面
        popular_pages = PageView.get_popular_pages(days=30)
        
        return Response({
            'success': True,
            'data': {
                'total_visitors': total_visitors,
                'total_pageviews': total_pageviews,
                'today_visitors': today_visitors,
                'today_pageviews': today_pageviews,
                'popular_pages': list(popular_pages),
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 管理頁面視圖
def analytics_dashboard(request):
    """分析儀表板頁面"""
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
    
    # 獲取統計數據（與admin中的邏輯類似）
    today = timezone.now().date()
    thirty_days_ago = today - timezone.timedelta(days=30)
    
    # 基本統計
    total_visitors = VisitorSession.objects.count()
    total_pageviews = PageView.objects.count()
    recent_visitors = VisitorSession.objects.filter(
        first_visit__date__gte=thirty_days_ago
    ).count()
    today_visitors = VisitorSession.objects.filter(
        first_visit__date=today
    ).count()
    
    # 熱門頁面
    popular_pages = PageView.objects.filter(
        visit_time__date__gte=thirty_days_ago
    ).values('page_path', 'page_title').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # 設備統計
    device_stats = VisitorSession.objects.filter(
        first_visit__date__gte=thirty_days_ago
    ).values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'total_visitors': total_visitors,
        'total_pageviews': total_pageviews,
        'recent_visitors': recent_visitors,
        'today_visitors': today_visitors,
        'popular_pages': popular_pages,
        'device_stats': device_stats,
    }
    
    return render(request, 'admin/analytics/dashboard.html', context)

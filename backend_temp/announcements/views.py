from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Announcement, AnnouncementCategory
from .serializers import (
    AnnouncementListSerializer, 
    AnnouncementDetailSerializer,
    AnnouncementCategorySerializer,
    AnnouncementHomepageSerializer
)


class AnnouncementListView(generics.ListAPIView):
    """公告列表API"""
    serializer_class = AnnouncementListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'priority', 'is_pinned']
    search_fields = ['title', 'summary']
    ordering_fields = ['publish_date', 'created_at', 'views_count']
    ordering = ['-is_pinned', '-publish_date']
    
    def get_queryset(self):
        """只返回可顯示的公告"""
        now = timezone.now()
        queryset = Announcement.objects.filter(
            status='published'
        ).filter(
            Q(publish_date__lte=now) | Q(publish_date__isnull=True)
        ).filter(
            Q(expire_date__gt=now) | Q(expire_date__isnull=True)
        ).select_related('category', 'author')
        
        return queryset


class AnnouncementDetailView(generics.RetrieveAPIView):
    """公告詳情API"""
    serializer_class = AnnouncementDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_queryset(self):
        """只返回可顯示的公告"""
        now = timezone.now()
        return Announcement.objects.filter(
            status='published'
        ).filter(
            Q(publish_date__lte=now) | Q(publish_date__isnull=True)
        ).filter(
            Q(expire_date__gt=now) | Q(expire_date__isnull=True)
        ).select_related('category', 'author').prefetch_related('additional_images')
    
    def retrieve(self, request, *args, **kwargs):
        """獲取公告詳情並增加瀏覽次數"""
        instance = self.get_object()
        # 增加瀏覽次數
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AnnouncementCategoryListView(generics.ListAPIView):
    """公告分類列表API"""
    queryset = AnnouncementCategory.objects.filter(is_active=True)
    serializer_class = AnnouncementCategorySerializer
    permission_classes = [AllowAny]
    ordering = ['order', 'name']


@api_view(['GET'])
@permission_classes([AllowAny])
def homepage_announcements(request):
    """首頁公告API - 返回最新的置頂和重要公告"""
    now = timezone.now()
    
    # 獲取置頂公告
    pinned_announcements = Announcement.objects.filter(
        status='published',
        is_pinned=True,
        show_on_homepage=True
    ).filter(
        Q(publish_date__lte=now) | Q(publish_date__isnull=True)
    ).filter(
        Q(expire_date__gt=now) | Q(expire_date__isnull=True)
    ).select_related('category')[:3]
    
    # 獲取最新公告（排除已顯示的置頂公告）
    pinned_ids = list(pinned_announcements.values_list('id', flat=True))
    recent_announcements = Announcement.objects.filter(
        status='published',
        show_on_homepage=True
    ).filter(
        Q(publish_date__lte=now) | Q(publish_date__isnull=True)
    ).filter(
        Q(expire_date__gt=now) | Q(expire_date__isnull=True)
    ).exclude(id__in=pinned_ids).select_related('category').order_by('-publish_date')[:5]
    
    # 序列化數據
    pinned_serializer = AnnouncementHomepageSerializer(
        pinned_announcements, 
        many=True, 
        context={'request': request}
    )
    recent_serializer = AnnouncementHomepageSerializer(
        recent_announcements, 
        many=True, 
        context={'request': request}
    )
    
    return Response({
        'pinned_announcements': pinned_serializer.data,
        'recent_announcements': recent_serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def announcement_stats(request):
    """公告統計API"""
    now = timezone.now()
    
    total_published = Announcement.objects.filter(status='published').count()
    total_categories = AnnouncementCategory.objects.filter(is_active=True).count()
    
    # 本月新增公告
    this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_announcements = Announcement.objects.filter(
        status='published',
        publish_date__gte=this_month
    ).count()
    
    return Response({
        'total_published': total_published,
        'total_categories': total_categories,
        'monthly_announcements': monthly_announcements
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def increment_likes(request, announcement_id):
    """增加公告點讚數"""
    try:
        announcement = get_object_or_404(Announcement, id=announcement_id, status='published')
        announcement.likes_count += 1
        announcement.save(update_fields=['likes_count'])
        
        return Response({
            'success': True,
            'likes_count': announcement.likes_count
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

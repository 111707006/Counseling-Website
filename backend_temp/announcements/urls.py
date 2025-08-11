from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    # 公告列表
    path('', views.AnnouncementListView.as_view(), name='announcement-list'),
    
    # 公告詳情
    path('<int:id>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
    
    # 公告分類列表
    path('categories/', views.AnnouncementCategoryListView.as_view(), name='category-list'),
    
    # 首頁公告
    path('homepage/', views.homepage_announcements, name='homepage-announcements'),
    
    # 公告統計
    path('stats/', views.announcement_stats, name='announcement-stats'),
    
]
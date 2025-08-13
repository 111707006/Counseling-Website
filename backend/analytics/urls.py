from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # API 端點
    path('api/track-visit/', views.track_visit, name='track_visit'),
    path('api/track-event/', views.track_event, name='track_event'),
    path('api/stats/', views.get_stats, name='get_stats'),
    
    # 管理頁面
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
]
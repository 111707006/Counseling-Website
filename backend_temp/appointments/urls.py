from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, test_appointment_create

# 創建DRF路由器
router = DefaultRouter()
# 註冊ViewSet：這會產生 /api/appointments/appointments/ 路徑（因為主urls.py中已有appointments/前綴）
router.register(r'', AppointmentViewSet, basename='appointment')  # 移除重複的'appointments'前綴

urlpatterns = [
    path('', include(router.urls)),  # 包含ViewSet路由
    path('test/', test_appointment_create, name='test-appointment-create'),  # 測試端點
]

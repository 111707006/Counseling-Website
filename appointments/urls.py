from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailableSlotViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'slots', AvailableSlotViewSet, basename='slot')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    # /api/appointments/slots/     GET: 可預約時段查詢
    # /api/appointments/appointments/        CRUD: 預約管理
    path('', include(router.urls)),
]

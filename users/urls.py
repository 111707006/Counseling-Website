from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    # 註冊新使用者（含指定 role：user / therapist）
    path('register/', RegisterView.as_view(), name='register'),

    # 登入並取得 JWT access + refresh
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 刷新 access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

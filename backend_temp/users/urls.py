from django.urls import path
# ※ 移除前台註冊與 token 路由（register/token/token/refresh）
# from .views import RegisterView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    # 註冊與登入改由預約流程自動處理
]

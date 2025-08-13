from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
# 註冊 ArticleViewSet，產生 /articles/、/articles/{pk}/ 等路由
router.register('articles', ArticleViewSet, basename='article')

urlpatterns = [
    # 掛載所有由 router 自動產生的路由
    path('', include(router.urls)),
]

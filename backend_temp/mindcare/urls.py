from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),                # JWT token、User 端點
    path('api/therapists/', include('therapists.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/assessments/', include('assessments.urls')),
    path('api/articles/', include('articles.urls')),
    path('api/', include('articles.urls')),
    path('api/auth/token/', obtain_auth_token),  # 登入 API
]

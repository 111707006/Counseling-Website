from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 其它 app 的路由...
    path('api/articles/', include('articles.urls')),
    #綠界 
    path('api/payments/', include('payments.urls', namespace='payments')),
 # 文章模組
]

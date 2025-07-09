from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import TherapistProfile
from .serializers import TherapistProfileSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class TherapistProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    心理師資料 ReadOnly API
    - GET /api/therapists/          取得所有心理師資料與時段列表
    - GET /api/therapists/{id}/     取得單一心理師介紹與時段
    """
    queryset = TherapistProfile.objects.prefetch_related('available_times').all().order_by('-created_at')
    serializer_class = TherapistProfileSerializer
    permission_classes = [AllowAny]

    # 加入搜尋、篩選和排序功能
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # 這裡可以增加多個篩選條件
    filterset_fields = [
        'consultation_modes',   # 支援線上/實體模式篩選
        'specialties',           # 支援專長篩選
        'title',                 # 支援頭銜篩選
    ]
    
    # 可以搜尋的字段，這裡可以加上更多字段
    search_fields = [
        'name',                  # 支援姓名搜尋
        'specialties',           # 支援專長搜尋
        'title',                 # 支援頭銜搜尋
        'beliefs',               # 支援信念/理念搜尋
    ]
    
    # 可排序欄位
    ordering_fields = ['created_at', 'name', 'title']  # 支援按建立時間、姓名、頭銜排序
    ordering = ['-created_at']  # 預設按創建時間倒序排序

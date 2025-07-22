from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import TherapistProfile, Specialty, SpecialtyCategory
from .serializers import TherapistProfileSerializer, SpecialtySerializer, SpecialtyCategorySerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class TherapistProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    心理師資料 ReadOnly API
    - GET /api/therapists/          取得所有心理師資料與時段列表
    - GET /api/therapists/{id}/     取得單一心理師介紹與時段
    """
    queryset = TherapistProfile.objects.prefetch_related(
        'available_times', 
        'specialties__category'
    ).all().order_by('-created_at')
    serializer_class = TherapistProfileSerializer
    permission_classes = [AllowAny]

    # 加入搜尋、篩選和排序功能
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # 篩選條件
    filterset_fields = [
       # 'consultation_modes',      # 支援線上/實體模式篩選
        'specialties',             # 支援專業領域篩選（關聯式）
        'specialties__category',   # 支援專業領域分類篩選
        'title',                   # 支援頭銜篩選
    ]
    
    # 搜尋字段
    search_fields = [
        'name',                    # 支援姓名搜尋
        'specialties__name',       # 支援專業領域名稱搜尋
        'specialties_text',        # 支援舊格式專長搜尋（向後相容）
        'title',                   # 支援頭銜搜尋
        'beliefs',                 # 支援信念/理念搜尋
    ]
    
    # 可排序欄位
    ordering_fields = ['created_at', 'name', 'title']  # 支援按建立時間、姓名、頭銜排序
    ordering = ['-created_at']  # 預設按創建時間倒序排序


class SpecialtyCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    專業領域分類 ReadOnly API
    - GET /api/therapists/specialty-categories/       取得所有專業領域分類
    - GET /api/therapists/specialty-categories/{id}/  取得單一分類
    """
    queryset = SpecialtyCategory.objects.all().order_by('name')
    serializer_class = SpecialtyCategorySerializer
    permission_classes = [AllowAny]


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    專業領域 ReadOnly API
    - GET /api/therapists/specialties/           取得所有專業領域
    - GET /api/therapists/specialties/{id}/      取得單一專業領域
    - 支援按分類篩選：?category={category_id}
    """
    queryset = Specialty.objects.select_related('category').filter(is_active=True).order_by('category__name', 'name')
    serializer_class = SpecialtySerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'category__name', 'created_at']
    ordering = ['category__name', 'name']

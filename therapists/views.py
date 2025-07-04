from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import TherapistProfile
from .serializers import TherapistProfileSerializer

class TherapistProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    心理師資料 ReadOnly API
    - GET /api/therapists/          取得所有心理師含時段列表
    - GET /api/therapists/{id}/     取得單一心理師介紹含時段
    """
    queryset = TherapistProfile.objects.prefetch_related('available_times').all().order_by('-created_at')
    serializer_class = TherapistProfileSerializer
    permission_classes = [AllowAny]

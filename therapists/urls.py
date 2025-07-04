from rest_framework.routers import DefaultRouter
from .views import TherapistProfileViewSet

router = DefaultRouter()
router.register(r'', TherapistProfileViewSet, basename='therapist')

urlpatterns = router.urls

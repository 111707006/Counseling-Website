from rest_framework.routers import DefaultRouter
from .views import TherapistProfileViewSet, SpecialtyViewSet

router = DefaultRouter()
router.register(r'profiles', TherapistProfileViewSet, basename='therapist-profile')
router.register(r'specialties', SpecialtyViewSet, basename='specialty')

urlpatterns = router.urls

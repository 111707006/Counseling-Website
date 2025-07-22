from rest_framework.routers import DefaultRouter
from .views import TherapistProfileViewSet, SpecialtyViewSet, SpecialtyCategoryViewSet

router = DefaultRouter()
router.register(r'profiles', TherapistProfileViewSet, basename='therapist-profile')
router.register(r'specialties', SpecialtyViewSet, basename='specialty')
router.register(r'specialty-categories', SpecialtyCategoryViewSet, basename='specialty-category')

urlpatterns = router.urls

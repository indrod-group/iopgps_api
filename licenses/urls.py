from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LicenseViewSet, UserLicenseReadAndCreate


router = DefaultRouter()
router.register(r'licenses', LicenseViewSet, basename='licenses')

router2 = DefaultRouter()
router2.register(r'licenses', UserLicenseReadAndCreate, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<str:uuid>/', include(router2.urls)),
]

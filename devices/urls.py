from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, UserDeviceReadViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'user-devices', UserDeviceReadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

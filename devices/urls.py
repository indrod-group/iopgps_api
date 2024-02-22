from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, UserPhoneDeviceList, UserDeviceReadViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'user-devices', UserDeviceReadViewSet)
phone_router = DefaultRouter()
phone_router.register(r'phones', UserPhoneDeviceList, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
    path('devices/<str:imei>/', include(phone_router.urls))
]

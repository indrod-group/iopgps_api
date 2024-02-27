from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BatteryViewSet, VehicleBatteryReadAndCreate


router = DefaultRouter()
router.register(r'batteries', BatteryViewSet, basename='batteries')

router2 = DefaultRouter()
router2.register(r'batteries', VehicleBatteryReadAndCreate, basename='vehicles')

urlpatterns = [
    path('', include(router.urls)),
    path('vehicles/<str:vuid>/', include(router2.urls)),
]

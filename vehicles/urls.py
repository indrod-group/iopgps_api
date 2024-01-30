from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BatteryViewSet,
    TireViewSet,
    UserVehicleReadViewSet,
    VehicleTypeViewSet,
    VehicleViewSet,
    VehicleStatusViewSet
)

router = DefaultRouter()
router.register(r'vehicletypes', VehicleTypeViewSet)
router.register(r'vehicles', VehicleViewSet)

router2 = DefaultRouter()
router2.register(r'tires', TireViewSet)
router2.register(r'batteries', BatteryViewSet)
router2.register(r'status', VehicleStatusViewSet)

router3 = DefaultRouter()
router3.register(r'vehicles', UserVehicleReadViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('vehicles/<str:pk>/', include(router2.urls)),
    path('users/<str:pk>/', include(router3.urls))
]

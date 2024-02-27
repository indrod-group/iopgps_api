from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserVehicleReadViewSet,
    VehicleTypeViewSet,
    VehicleViewSet,
)

router = DefaultRouter()
router.register(r'vehicletypes', VehicleTypeViewSet)
router.register(r'vehicles', VehicleViewSet)
router3 = DefaultRouter()
router3.register(r'vehicles', UserVehicleReadViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<str:pk>/', include(router3.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleRegistrationViewSet

router = DefaultRouter()
router.register(r'vehicleregistration', VehicleRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

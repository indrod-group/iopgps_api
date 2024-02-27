from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MileageViewSet, VehicleMileageReadAndCreate


router = DefaultRouter()
router.register(r'mileages', MileageViewSet, basename='mileages')

router2 = DefaultRouter()
router2.register(r'mileages', VehicleMileageReadAndCreate, basename='vehicles')

urlpatterns = [
    path('', include(router.urls)),
    path('vehicles/<str:vuid>/', include(router2.urls)),
]

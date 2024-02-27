from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TireViewSet, VehicleTireReadAndCreate


router = DefaultRouter()
router.register(r'tires', TireViewSet, basename='tires')

router2 = DefaultRouter()
router2.register(r'tires', VehicleTireReadAndCreate, basename='vehicles')

urlpatterns = [
    path('', include(router.urls)),
    path('vehicles/<str:vuid>/', include(router2.urls)),
]

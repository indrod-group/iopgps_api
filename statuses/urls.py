from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleStatusViewSet, VehicleStatusReadAndCreate


router = DefaultRouter()
router.register(r'statuses', VehicleStatusViewSet, basename='statuses')

router2 = DefaultRouter()
router2.register(r'statuses', VehicleStatusReadAndCreate, basename='vehicles')

urlpatterns = [
    path('', include(router.urls)),
    path('vehicles/<str:vuid>/', include(router2.urls)),
]

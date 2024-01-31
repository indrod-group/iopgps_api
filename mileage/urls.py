from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MileageViewSet

router = DefaultRouter()
router.register(r'mileages', MileageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

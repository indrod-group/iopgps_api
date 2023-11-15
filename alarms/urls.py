from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlarmViewSet

router = DefaultRouter()
router.register(r"alarms", AlarmViewSet, basename="alarm")

urlpatterns = [
    path("", include(router.urls)),
]

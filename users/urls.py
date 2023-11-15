from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, ChangePasswordViewSet

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="user")
router.register(r"change-password", ChangePasswordViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

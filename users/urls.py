from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet,
    ChangePasswordViewSet,
    CustomUserTreeViewSet
)

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="user")
router.register(r"change-password", ChangePasswordViewSet)

router2 = DefaultRouter()
router2.register(r"tree/accounts", CustomUserTreeViewSet, basename='user-tree')

urlpatterns = [
    path("", include(router.urls)),
    path("users/<str:pk>/", include(router2.urls)),
]

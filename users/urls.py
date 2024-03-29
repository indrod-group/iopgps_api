from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet,
    ChangePasswordViewSet,
    CustomUserTreeViewSet,
    PhoneNumberViewSet
)

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="users")
router.register(r"change-password", ChangePasswordViewSet)

router2 = DefaultRouter()
router2.register(r"tree/accounts", CustomUserTreeViewSet, basename='user-tree')
router2.register(r"phonenumbers", PhoneNumberViewSet, basename="phonenumber")
urlpatterns = [
    path("", include(router.urls)),
    path("users/<str:pk>/", include(router2.urls)),
]

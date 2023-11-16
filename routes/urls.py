from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReadOnlyRouteViewSet, UserDeviceReadViewSet

router = DefaultRouter()
router.register(r'routes', ReadOnlyRouteViewSet, basename='route')
router.register(r'user-routes', UserDeviceReadViewSet, basename='user-route')

urlpatterns = [
    path('', include(router.urls)),
]

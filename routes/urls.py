from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import  UserRouteReadAndCreate, RouteViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet)

router2 = DefaultRouter()
router2.register(r'routes', UserRouteReadAndCreate, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<str:uuid>/', include(router2.urls)),
]

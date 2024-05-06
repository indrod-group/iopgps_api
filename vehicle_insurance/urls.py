from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrokerInfoViewSet

router = DefaultRouter()
router.register(r'brokerinfo', BrokerInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

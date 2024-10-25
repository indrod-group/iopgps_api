from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrokerInfoViewSet, BrokerInfoReadAndCreate

router = DefaultRouter()
router.register(r"brokerinfo", BrokerInfoViewSet)

router2 = DefaultRouter()
router2.register(r"brokerinfo", BrokerInfoReadAndCreate, basename="vehicles")

urlpatterns = [
    path("", include(router.urls)),
    path("vehicles/<str:vuid>/", include(router2.urls)),
]

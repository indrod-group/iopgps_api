from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IncidentViewSet,
    MovementOrderStateViewSet,
    MovementOrderViewSet,
    ClosureMovementOrderViewSet,
)

router = DefaultRouter()
router.register(r"orders", MovementOrderViewSet, basename="orders")
router.register(r"closures", ClosureMovementOrderViewSet, basename="closures")
router.register(r"states", MovementOrderStateViewSet, basename="states")
router.register(r"incidents", IncidentViewSet, basename="incidents")

urlpatterns = [
    path("movements/", include(router.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    MaintenanceManualViewSet,
    MaintenanceOperationViewSet,
    VehicleManualReadAndCreateView,
    VehicleManualReadView
)

router = DefaultRouter()
router.register(r"manuals", MaintenanceManualViewSet, basename="manuals")
router.register(r"operations", MaintenanceOperationViewSet, basename="operations")

router2 = DefaultRouter()
router2.register(r"manuals", VehicleManualReadAndCreateView, basename="types")

router3 = DefaultRouter()
router3.register(r"manuals", VehicleManualReadView, basename="vehicles")

urlpatterns = [
    path("", include(router.urls)),
    path("vehicles/types/<int:id>/", include(router2.urls)),
    path("vehicles/<str:brand>/<str:model>/<int:year>/", include(router3.urls))
]

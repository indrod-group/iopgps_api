from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceManualViewSet, MaintenanceOperationViewSet

router = DefaultRouter()
router.register(r'manuals', MaintenanceManualViewSet)
router.register(r'operations', MaintenanceOperationViewSet)

urlpatterns = [
    path('maintenance', include(router.urls)),
]

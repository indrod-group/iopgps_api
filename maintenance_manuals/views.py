from typing import Optional
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from vehicles.models import VehicleType
from .models import MaintenanceManual, MaintenanceOperation
from .serializers import MaintenanceManualSerializer, MaintenanceOperationSerializer

class MaintenanceManualViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for the MaintenanceManual model.
    It provides standard actions for interacting with MaintenanceManual instances.
    """

    serializer_class = MaintenanceManualSerializer
    queryset = MaintenanceManual.objects.all()


class MaintenanceOperationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for the MaintenanceOperation model.
    It provides standard actions for interacting with MaintenanceOperation instances.
    """

    queryset = MaintenanceOperation.objects.all()
    serializer_class = MaintenanceOperationSerializer


class VehicleManualReadAndCreateView(
    viewsets.ReadOnlyModelViewSet, viewsets.mixins.CreateModelMixin
):
    serializer_class = MaintenanceManualSerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of Manual objects for the vehicle specified by the 'pk' parameter in the URL,
        which corresponds to the 'id' of the vehicle type. If the 'id' is None or does not exist, it returns an empty queryset.
        """
        vid: Optional[str] = self.kwargs.get("id", None)
        if vid is not None:
            vehicletype = get_object_or_404(VehicleType, id=vid)
            return MaintenanceManual.objects.filter(vehicle_type=vehicletype)
        return MaintenanceManual.objects.none()


class VehicleManualReadView(
    viewsets.ReadOnlyModelViewSet,
):
    serializer_class = MaintenanceManualSerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of Manual objects for the vehicle specified by the 'year', 'brand', and 'model' parameters in the URL.
        If any of these parameters are None or do not exist, it returns an empty queryset.
        """
        year: Optional[str] = self.kwargs.get("year", None)
        brand: Optional[str] = self.kwargs.get("brand", None)
        model: Optional[str] = self.kwargs.get("model", None)

        if year and brand and model:
            vehicletype = get_object_or_404(
                VehicleType, year=year, brand=brand, model=model
            )
            return MaintenanceManual.objects.filter(vehicle_type=vehicletype)
        return MaintenanceManual.objects.none()

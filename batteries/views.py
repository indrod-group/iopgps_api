from typing import Optional
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from vehicles.models import Battery, Vehicle
from .serializers import BatterySerializer

class BatteryViewSet(viewsets.ModelViewSet):
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer

class VehicleBatteryReadAndCreate(
    viewsets.ReadOnlyModelViewSet,
    viewsets.mixins.CreateModelMixin
):
    serializer_class = BatterySerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of Battery objects
        for the vehicle specified by the 'pk' parameter in the URL,
        which corresponds to the 'vuid' of the vehicle.
        If the 'vuid' is None or does not exist, it returns an empty queryset.
        """
        vuid: Optional[str] = self.kwargs.get("vuid")
        if vuid is not None:
            vehicle = get_object_or_404(Vehicle, vuid=vuid)
            return Battery.objects.filter(vehicle=vehicle)
        return Battery.objects.none()

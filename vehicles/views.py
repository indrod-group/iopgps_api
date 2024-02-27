from typing import Optional
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from users.models import CustomUser

from .models import (
    Battery,
    Tire,
    VehicleStatus,
    VehicleType,
    Vehicle
)
from .serializers import (
    VehicleBatterySerializer,
    TireSerializer,
    VehicleStatusSerializer,
    VehicleTypeSerializer,
    VehicleSerializer
)

class UserVehicleReadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing the vehicles associated with a user.
    """

    serializer_class = VehicleSerializer

    def get_queryset(self):
        """
        Retrieve the vehicles associated with the user specified by the UUID.
        If the UUID does not exist, return an error.
        If the user has no associated vehicles, return an empty list.
        """
        pk: Optional[str] = self.kwargs.get("pk")
        if pk is not None:
            user = get_object_or_404(CustomUser, uuid=pk)
            return Vehicle.objects.filter(uservehicle__user=user)
        return Vehicle.objects.none() 

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleStatusViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing vehicle status instances.
    """
    serializer_class = VehicleStatusSerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of VehicleStatus objects
        for the vehicle specified by the 'pk' parameter in the URL,
        which corresponds to the 'vuid' of the vehicle.
        If the 'vuid' is None or does not exist, it returns an empty queryset.
        """
        vuid: Optional[str] = self.kwargs.get("pk")
        if vuid is not None:
            vehicle = get_object_or_404(Vehicle, vuid=vuid)
            return VehicleStatus.objects.filter(vehicle=vehicle)
        return VehicleStatus.objects.none()


class VehicleTireReadAndCreate(
    viewsets.ReadOnlyModelViewSet,
    viewsets.mixins.CreateModelMixin
):
    serializer_class = TireSerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of Tire objects
        for the vehicle specified by the 'pk' parameter in the URL,
        which corresponds to the 'vuid' of the vehicle.
        If the 'vuid' is None or does not exist, it returns an empty queryset.
        """
        vuid: Optional[str] = self.kwargs.get("vuid")
        if vuid is not None:
            vehicle = get_object_or_404(Vehicle, vuid=vuid)
            return Tire.objects.filter(vehicle=vehicle)
        return Tire.objects.none()

    def get_object(self):
        vuid = self.kwargs.get('vuid')
        tire_id = self.kwargs.get('id')
        if vuid is not None and tire_id is not None:
            vehicle = get_object_or_404(Vehicle, vuid=vuid)
            return get_object_or_404(Tire, vehicle=vehicle, id=tire_id)
        return None

class VehicleBatteryReadAndCreate(
    viewsets.ReadOnlyModelViewSet,
    viewsets.mixins.CreateModelMixin
):
    serializer_class = VehicleBatterySerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of Battery objects
        for the vehicle specified by the 'pk' parameter in the URL,
        which corresponds to the 'vuid' of the vehicle.
        If the 'vuid' is None or does not exist, it returns an empty queryset.
        """
        vuid: Optional[str] = self.kwargs.get("pk")
        if vuid is not None:
            vehicle = get_object_or_404(Vehicle, vuid=vuid)
            return Battery.objects.filter(vehicle=vehicle)
        return Battery.objects.none()

    def get_object(self):
        vuid = self.kwargs.get('vuid')
        tire_id = self.kwargs.get('id')
        if vuid is not None and tire_id is not None:
            vehicle = get_object_or_404(Vehicle, vuid=vuid)
            return get_object_or_404(Battery, vehicle=vehicle, id=tire_id)
        return None

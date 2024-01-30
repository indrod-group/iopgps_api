from typing import Optional
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from users.models import CustomUser

from .models import (
    Battery,
    Tire,
    UserVehicle,
    VehicleStatus,
    VehicleType,
    Vehicle
)
from .serializers import (
    BatterySerializer,
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
            user_vehicles = UserVehicle.objects.filter(user=user)
            vehicles = [user_vehicle.vehicle for user_vehicle in user_vehicles]
            return vehicles
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
    queryset = VehicleStatus.objects.all()
    serializer_class = VehicleStatusSerializer

class TireViewSet(viewsets.ModelViewSet):
    queryset = Tire.objects.all()
    serializer_class = TireSerializer

class BatteryViewSet(viewsets.ModelViewSet):
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer

from typing import Optional
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from vehicles.models import Vehicle
from .models import BrokerInfo
from .serializers import BrokerInfoSerializer

class BrokerInfoViewSet(viewsets.ModelViewSet):
    queryset = BrokerInfo.objects.all()
    serializer_class = BrokerInfoSerializer


class BrokerInfoReadAndCreate(
    viewsets.ReadOnlyModelViewSet,
    viewsets.mixins.CreateModelMixin
):
    serializer_class = BrokerInfoSerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of BrokerInfo objects
        for the vehicle specified by the 'pk' parameter in the URL,
        which corresponds to the 'vuid' of the vehicle.
        If the 'vuid' is None or does not exist, it returns an empty queryset.
        """
        vuid: Optional[str] = self.kwargs.get("vuid")
        if vuid is not None:
            vehicle = get_object_or_404(Vehicle, vuid=vuid)
            return BrokerInfo.objects.filter(vehicle=vehicle)
        return BrokerInfo.objects.none()

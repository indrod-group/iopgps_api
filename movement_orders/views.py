from rest_framework import viewsets
from .models import (
    Incident,
    MovementOrder,
    ClosureMovementOrder,
    MovementOrderState,
)
from .serializers import (
    IncidentSerializer,
    MovementOrderSerializer,
    ClosureMovementOrderSerializer,
    MovementOrderStateSerializer,
)


class MovementOrderViewSet(viewsets.ModelViewSet):
    queryset = MovementOrder.objects.all()
    serializer_class = MovementOrderSerializer


class MovementOrderStateViewSet(viewsets.ModelViewSet):
    queryset = MovementOrderState.objects.all()
    serializer_class = MovementOrderStateSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class ClosureMovementOrderViewSet(viewsets.ModelViewSet):
    queryset = ClosureMovementOrder.objects.all()
    serializer_class = ClosureMovementOrderSerializer

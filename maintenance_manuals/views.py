from rest_framework import viewsets
from .models import MaintenanceManual, MaintenanceOperation
from .serializers import MaintenanceManualSerializer, MaintenanceOperationSerializer

class MaintenanceManualViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceManual.objects.all()
    serializer_class = MaintenanceManualSerializer

class MaintenanceOperationViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceOperation.objects.all()
    serializer_class = MaintenanceOperationSerializer

from rest_framework import viewsets
from .models import WorkOrder, WorkOrderCompletion
from .serializers import WorkOrderSerializer, WorkOrderCompletionSerializer

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

class WorkOrderCompletionViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderCompletion.objects.all()
    serializer_class = WorkOrderCompletionSerializer

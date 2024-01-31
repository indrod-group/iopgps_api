from rest_framework import serializers
from .models import WorkOrder, WorkOrderCompletion

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'

class WorkOrderCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderCompletion
        fields = '__all__'

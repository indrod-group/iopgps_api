from rest_framework import serializers
from .models import MaintenanceManual, MaintenanceOperation

class MaintenanceOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceOperation
        fields = '__all__'

class MaintenanceManualSerializer(serializers.ModelSerializer):
    manual_tasks = MaintenanceOperationSerializer(many=True, read_only=True)

    class Meta:
        model = MaintenanceManual
        fields = '__all__'

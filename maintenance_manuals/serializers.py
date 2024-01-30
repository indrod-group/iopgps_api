from rest_framework import serializers
from .models import MaintenanceManual, MaintenanceOperation

class MaintenanceManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceManual
        fields = '__all__'

class MaintenanceOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceOperation
        fields = '__all__'

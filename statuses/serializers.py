from rest_framework import serializers
from vehicles.models import VehicleStatus

class VehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStatus
        fields = '__all__'

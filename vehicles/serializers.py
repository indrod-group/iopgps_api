from rest_framework import serializers

from devices.serializers import DeviceSerializer
from .models import (
    Battery,
    Tire,
    UserVehicle,
    VehicleStatus,
    VehicleType,
    Vehicle
)


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = [
            "year",
            "brand",
            "model",
            "version",
            "fuel_type",
            "city_mileage",
            "highway_mileage",
            "mixed_mileage",
        ]


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_type = VehicleTypeSerializer()
    device = DeviceSerializer()

    class Meta:
        model = Vehicle
        fields = [
            "vuid",
            "vehicle_type",
            "device",
            "color",
            "chassis",
            "plate",
            "tonnage",
            "vin",
        ]


class VehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStatus
        fields = ["vehicle", "condition", "status_updated_at"]


class UserVehicleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = UserVehicle
        fields = [
            "user",
            "vehicles",
        ]


class TireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tire
        fields = [
            "vehicle",
            "manufacturing_code",
            "position_relative_to_vehicle",
            "registration_date",
            "in_use",
            "location",
            "notes",
            "manufacturer",
            "cost",
        ]


class BatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = [
            "vehicle", 
            "manufacturing_code",
            "registration_date",
            "in_use",
            "location",
            "notes",
            "manufacturer",
            "cost",
        ]

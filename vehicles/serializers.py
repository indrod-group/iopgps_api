from collections import OrderedDict
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
            "front_photo",
            "left_side_photo",
            "right_side_photo",
            "rear_photo",
        ]


class VehicleStatusSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        write_only=True
    )

    class Meta:
        model = VehicleStatus
        fields = ["vehicle", "condition", "status_updated_at"]

    def create(self, validated_data: OrderedDict):
        return VehicleStatus.objects.create(**validated_data)

    update = None
    partial_update = None

class UserVehicleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = UserVehicle
        fields = [
            "user",
            "vehicles",
        ]

    create = None
    update = None
    partial_update = None

class TireSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        write_only=True
    )

    class Meta:
        model = Tire
        fields = [
            "id",
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

    def create(self, validated_data: OrderedDict):
        return Tire.objects.create(**validated_data)

    update = None
    partial_update = None

class VehicleBatterySerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        write_only=True
    )

    class Meta:
        model = Battery
        fields = [
            "id",
            "vehicle", 
            "manufacturing_code",
            "registration_date",
            "in_use",
            "location",
            "notes",
            "manufacturer",
            "cost",
        ]

    def create(self, validated_data: OrderedDict):
        return Battery.objects.create(**validated_data)

    update = None
    partial_update = None

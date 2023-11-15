from rest_framework import serializers
from .models import Device, UserDevice


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Device model. This serializer includes all fields in the Device model
    and supports all CRUD (Create, Retrieve, Update, Delete) operations.
    """

    class Meta:
        model = Device
        fields = "__all__"


class UserDeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserDevice model. This serializer includes the user and device fields,
    which are foreign keys to the CustomUser and Device models respectively.
    """

    user = serializers.StringRelatedField()
    devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = UserDevice
        fields = [
            "user",
            "devices",
        ]

from rest_framework import serializers
from users.models import PhoneNumber

from users.serializers import PhoneNumberSerializer
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


class UserPhoneDeviceSerializer(serializers.ModelSerializer):
    """
    A serializer for the UserDevice model.

    This serializer includes a method field 'phone_numbers' which represents
    the phone numbers associated with the user of the UserDevice.
    """
    phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = UserDevice
        fields = ['user', 'phone_numbers',]

    def get_phone_numbers(self, obj):
        """
        Retrieves the phone numbers associated with the user of the UserDevice.

        Args:
            obj (UserDevice): The UserDevice instance being serialized.

        Returns:
            list: A list of phone numbers associated with the user of the UserDevice.
        """
        phone_numbers = PhoneNumber.objects.filter(user=obj.user)
        return PhoneNumberSerializer(phone_numbers, many=True).data

from collections import OrderedDict
import os
from typing import Optional
from time import time

import requests
from django.db.models import Q
from rest_framework import serializers

from devices.models import Device

from .models import Alarm


TEN_METER_IN_GRADES = 0.00008983111


def get_address(lat: str, lng: str):
    """
    Makes a reverse geocoding request to Geoapify
    to get the address of a location given by its latitude and longitude.

    Parameters:
        - lat (str): The latitude of the location.
        - lng (str): The longitude of the location.

    Returns:
        - str: The address of the location if the request was successful, None otherwise.
    """
    existing_alarm = Alarm.objects.filter(
        Q(lat__gte=float(lat) - TEN_METER_IN_GRADES)
        & Q(lat__lte=float(lat) + TEN_METER_IN_GRADES)
        & Q(lng__gte=float(lng) - TEN_METER_IN_GRADES)
        & Q(lng__lte=float(lng) + TEN_METER_IN_GRADES)
    ).first()
    if existing_alarm is not None:
        return existing_alarm.address
    try:
        api_key = os.getenv("GEOAPIFY_KEY")
        response = requests.get(
            f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lng}&apiKey={api_key}",
            timeout=5000,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error making the request to Geoapify: {e}")
        return None

    data = response.json()
    if data["features"]:
        first_feature = data["features"][0]
        if "properties" in first_feature and "formatted" in first_feature["properties"]:
            return first_feature["properties"]["formatted"]

    return None


class AlarmSerializer(serializers.ModelSerializer):
    """
    Serializer for the Alarm model. This serializer only supports read and create operations.
    Update and partial update operations are not allowed.
    """

    device_imei = serializers.CharField(source="device.imei", write_only=True)

    class Meta:
        model = Alarm
        fields = [
            "id",
            "device_imei",
            "lat",
            "lng",
            "time",
            "address",
            "alarm_code",
            "alarm_type",
            "course",
            "device_type",
            "position_type",
            "speed",
        ]
        read_only_fields = ("id",)

    def create(self, validated_data: OrderedDict):
        """
        Create a new alarm instance. If latitude and longitude are provided,
        make a reverse geocoding request to Geoapify to get the address.
        """
        device_imei = validated_data.pop("device")["imei"]
        device = Device.objects.get(imei=device_imei)

        lat = validated_data.get("lat", None)
        lng = validated_data.get("lng", None)
        address: Optional[str] = validated_data.get("address", None)
        alarm_time = validated_data.get("time", int(time()))
        current_time = int(time())

        def is_today_the_alarm():
            return current_time - 86400 <= alarm_time <= current_time

        def is_address_empty():
            return (
                lat is not None
                and lng is not None
                and (address is None or address == "")
            )

        if is_today_the_alarm() and is_address_empty():
            validated_data["address"] = get_address(lat, lng)

        alarm = Alarm.objects.create(device=device, **validated_data)
        return alarm

    def update(self, instance, validated_data):
        """
        Overwrites the update method to prevent partial updates.
        """
        raise NotImplementedError("Update operation is not allowed.")

    def partial_update(self, instance, validated_data):
        """
        Overwrites the partial_update method to prevent partial updates.
        """
        raise NotImplementedError("Partial update operation is not allowed.")

from collections import OrderedDict
from datetime import datetime, timedelta
import os

import requests
from rest_framework import serializers

from devices.models import Device

from .models import Alarm

T24_HOURS = timedelta(hours=24)

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

        lat = validated_data.get("lat")
        lng = validated_data.get("lng")
        time = validated_data.get("time")

        # Convert the alarm time to a datetime object
        alarm_time = datetime.fromtimestamp(time)

        # Get the current time
        now = datetime.now()

        # Check if the alarm time is within the last 24 hours
        if lat is not None and lng is not None and now - T24_HOURS <= alarm_time <= now:
            api_key = os.getenv("GEOAPIFY_KEY")
            # Make a reverse geocoding request to Geoapify
            response = requests.get(
                (
                    "https://api.geoapify.com/v1/geocode/reverse?"
                    f"lat={lat}&lon={lng}&apiKey={api_key}"
                ),
                timeout=5000,
            )
            data = response.json()

            # If the request was successful, get the address from the response
            if response.status_code == 200 and data["features"]:
                first_feature = data["features"][0]
                if "properties" in first_feature and "formatted" in first_feature["properties"]:
                    validated_data["address"] = first_feature["properties"]["formatted"]

        alarm = Alarm.objects.create(device=device, **validated_data)
        return alarm

    def update(self, instance, validated_data):
        """
        Update an existing alarm instance.
        If latitude, longitude, time, and alarm_code are the same,
        and the address is either blank or null,
        make a reverse geocoding request to Geoapify to update the address.
        """
        lat = validated_data.get("lat")
        lng = validated_data.get("lng")
        time = validated_data.get("time")
        alarm_code = validated_data.get("alarm_code")

        # Check if the alarm instance has the same lat, lng, time, and alarm_code
        if (
            instance.lat == lat
            and instance.lng == lng
            and instance.time == time
            and instance.alarm_code == alarm_code
        ):
            # Check if the address is either blank or null
            if not instance.address:
                api_key = os.getenv("GEOAPIFY_KEY")
                # Make a reverse geocoding request to Geoapify
                response = requests.get(
                    (
                        "https://api.geoapify.com/v1/geocode/reverse?"
                        f"lat={lat}&lon={lng}&apiKey={api_key}"
                    ),
                    timeout=5000,
                )
                data = response.json()

                # If the request was successful, get the address from the response
                if response.status_code == 200 and data["features"]:
                    first_feature = data["features"][0]
                    if "properties" in first_feature and "formatted" in first_feature["properties"]:
                        instance.address = first_feature["properties"]["formatted"]
                        instance.save()

        return instance

    def partial_update(self, instance, validated_data):
        """
        Overwrites the partial_update method to prevent partial updates.
        """
        raise NotImplementedError("Partial update operation is not allowed.")

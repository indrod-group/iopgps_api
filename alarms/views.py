from datetime import timedelta
from typing import Optional

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Alarm, Device
from .serializers import AlarmSerializer, get_address
from .utils import fix_range_times


class AlarmViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and creating alarms. Each alarm is associated with a device and
    contains information about the geographic coordinates, the type of alarm, and other details.
    The viewset supports filtering by alarm code, alarm time, imei, and time range.
    The viewset does not allow update or destroy operations.
    """

    serializer_class = AlarmSerializer

    def get_queryset(self):
        """
        Get the queryset for the alarms, applying the necessary filters and optimizations.
        """
        imei: Optional[str] = self.request.query_params.get("imei", None)
        if imei is None:
            raise ValidationError({"detail": "imei is required."})

        if not Device.objects.filter(imei=imei).exists():
            raise ValidationError(
                {"detail": "imei from a registered device is required."}
            )

        queryset = Alarm.objects.select_related("device")
        queryset = queryset.filter(device__imei=imei)

        alarm_codes: Optional[str] = self.request.query_params.get("alarm_codes", None)
        if alarm_codes is not None:
            alarm_codes = alarm_codes.split(",")
            queryset = queryset.filter(alarm_code__in=alarm_codes)

        last_alarms: bool = (
            self.request.query_params.get("last_alarms", "false").lower() == "true"
        )
        if last_alarms:
            seconds = int(self.request.query_params.get("seconds", "120"))
            time_ago = timezone.now() - timedelta(seconds=seconds)
            time_ago_unix = int(time_ago.timestamp())
            queryset = queryset.filter(time__gte=time_ago_unix)
        else:
            start_time = self.request.query_params.get("start_time", None)
            end_time = self.request.query_params.get(
                "end_time", int(timezone.now().timestamp())
            )
            start_time, end_time = fix_range_times(start_time, end_time)
            if start_time is not None:
                queryset = queryset.filter(time__range=(start_time, end_time))

        return queryset

    def __update_address_in_alarm(self, alarm: Alarm):
        """Updates the address of an alarm if needed."""
        lat = alarm.lat
        lng = alarm.lng
        address = alarm.address
        if lat is None or lng is None:
            return alarm

        if address is not None:
            return alarm

        if address != "":
            return alarm

        alarm.address = get_address(lat, lng)

        return alarm

    def create(self, request: Request, *args, **kwargs):
        """
        Create a new alarm instance with the data provided in the request.
        If an existing alarm instance with the same imei, alarm_time,
        and alarm_code exists, update that instance.
        """
        imei = request.data.get("device_imei")
        alarm_time = request.data.get("time")
        alarm_code = request.data.get("alarm_code")

        # Get the device associated with the imei
        device = Device.objects.get(imei=imei)

        # Try to get an existing alarm instance
        existing_alarm = Alarm.objects.filter(
            device=device, time=alarm_time, alarm_code=alarm_code
        ).first()

        if existing_alarm is not None:
            existing_alarm = self.__update_address_in_alarm(existing_alarm)
            existing_alarm.save(force_update=True)
            serializer = self.get_serializer(existing_alarm)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Overwrites the update method to prevent updates.
        Returns a 405 error for any update request.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        Overwrites the destroy method to prevent deletes.
        Returns a 405 error for any delete request.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

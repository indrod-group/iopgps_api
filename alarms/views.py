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

    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

    def filter_queryset_by_alarm_code(self, request: Request):
        """
        Filter the queryset by the alarm codes specified in the request query parameters.
        The alarm codes should be comma-separated strings.
        """
        alarm_codes: Optional[str] = request.query_params.get("alarm_codes")
        if alarm_codes is not None:
            alarm_codes = alarm_codes.split(",")
            self.queryset = self.queryset.filter(alarm_code__in=alarm_codes)

    def filter_queryset_by_alarm_time(self, request: Request):
        """
        Filter the queryset by the alarm time specified in the request query parameters.
        The alarm time should be a boolean indicating whether to return only the last alarms
        within a given number of seconds. The default value for the number of seconds is 120.
        """
        last_alarms: bool = (
            request.query_params.get("last_alarms", "false").lower() == "true"
        )
        if last_alarms:
            seconds = int(request.query_params.get("seconds", "120"))
            time_ago = timezone.now() - timedelta(seconds=seconds)
            time_ago_unix = int(time_ago.timestamp())
            self.queryset = self.queryset.filter(time__gte=time_ago_unix)
            return last_alarms

    def filter_queryset_by_imei(self, request: Request):
        """
        Filter the queryset by the imei specified in the request query parameters.
        The imei should be a string representing the unique identifier of the device.
        """
        imei = request.query_params.get("imei", None)
        if imei is None:
            raise ValidationError({"detail": "imei is required."})

        if not Device.objects.filter(imei=imei).exists():
            raise ValidationError({"detail": "imei from a registered device is required."})

        self.queryset = self.queryset.filter(device__imei=imei)

    def filter_queryset_by_time_range(self, request: Request):
        """
        Filter the queryset by the time range specified in the request query parameters.
        The time range should be two integers representing the start and end time in unix format.
        The default value for the end time is the current time.
        """
        start_time = request.query_params.get("start_time", None)
        end_time = request.query_params.get("end_time", int(timezone.now().timestamp()))
        start_time, end_time = fix_range_times(start_time, end_time)
        if start_time is not None:
            self.queryset = self.queryset.filter(time__range=(start_time, end_time))

    def list(self, request, *args, **kwargs):
        """
        List the alarms that match the filtering criteria in the request query parameters.
        If the last_alarms filter is applied, the time_range filter is ignored.
        The alarm_code and imei filters are applied if specified.
        """
        self.filter_queryset_by_imei(request)
        if not self.filter_queryset_by_alarm_time(request):
            self.filter_queryset_by_time_range(request)
        self.filter_queryset_by_alarm_code(request)
        return super().list(request, *args, **kwargs)

    def get_existing_alarm(self, imei, alarm_time, alarm_code):
        """
        Get an existing alarm instance that matches the given imei, alarm_time, and alarm_code.
        If no such instance exists, return None.
        """
        return Alarm.objects.filter(
            device__imei=imei, time=alarm_time, alarm_code=alarm_code
        ).first()

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
        If an existing alarm instance with the same imei, alarm_time, and alarm_code exists,
        return that instance instead with a 208 status code.
        """
        imei = request.data.get("device_imei")
        alarm_time = request.data.get("time")
        alarm_code = request.data.get("alarm_code")

        existing_alarm = self.get_existing_alarm(imei, alarm_time, alarm_code)
        if existing_alarm is not None:
            existing_alarm = self.__update_address_in_alarm(existing_alarm)
            existing_alarm.save(force_update=True)
            serializer = self.get_serializer(existing_alarm)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_208_ALREADY_REPORTED,
                headers=headers,
            )

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

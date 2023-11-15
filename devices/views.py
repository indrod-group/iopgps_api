from collections import namedtuple

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Device, UserDevice, CustomUser
from .serializers import (
    DeviceSerializer,
    UserDeviceSerializer,
)

GetParam = namedtuple("str", ["param", "default_value", "description", "true_value"])

IS_TRACKING_ALARMS_PARAM = GetParam(
    "is_tracking_alarms", "false", "Track only alarms from devices.", "true"
)


class UserDeviceReadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing the devices associated with a user.
    The retrieve method has been overridden to return only the IMEIs
    of the devices associated with the user specified by the UUID.
    """

    queryset = UserDevice.objects.all()
    serializer_class = UserDeviceSerializer

    def list(self, request, *args, **kwargs):
        """
        Override the list method to return a 405 error for GET requests to the base URL.
        """
        return Response(
            {"detail": 'Method "GET" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the devices associated with the user specified by the UUID.
        If the UUID does not exist, return an error.
        If the user has no associated devices, return an empty list.
        """
        user = get_object_or_404(CustomUser, uuid=kwargs["pk"])
        user_devices = UserDevice.objects.filter(user=user)

        if not user_devices.exists():
            return Response([])

        devices = [user_device.device for user_device in user_devices]
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


class DeviceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing device instances.
    """

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def __filter_queryset_by_tracking_alarms(self, request: Request):
        """
        Filters the queryset based on the 'is_tracking_alarms' request parameter.
        """
        param: str = request.query_params.get(
            IS_TRACKING_ALARMS_PARAM.param, IS_TRACKING_ALARMS_PARAM.default_value
        )
        is_tracking_alarms: bool = param.lower() == IS_TRACKING_ALARMS_PARAM.true_value
        self.queryset = self.queryset.filter(is_tracking_alarms=is_tracking_alarms)

    def list(self, request, *args, **kwargs):
        """
        This method is used to retrieve the query for this endpoint.
        Filters the devices based on the 'is_tracking', 'is_tracking_alarms'
        and 'is_tracking_locations' request parameters.
        """
        self.__filter_queryset_by_tracking_alarms(request)
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        """
        Creates a new device or updates an existing one based on the 'imei' request parameter.
        """
        imei = request.data.get("imei")
        if imei is not None:
            device, _ = Device.objects.update_or_create(
                imei=imei, defaults=request.data
            )
            serializer = self.get_serializer(device)
            return Response(serializer.data, status=status.HTTP_208_ALREADY_REPORTED)

        # If the imei does not exist, we create a new user
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        """
        Updates the data of an existing device based on the 'imei' request parameter.
        """
        imei = request.data.get("imei")
        if imei is not None:
            device = Device.objects.filter(imei=imei).first()
            if device is not None:
                # If the user exists, we update their data
                serializer = self.get_serializer(device, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)

        # If the imei does not exist or the user does not exist, we return an error
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Implement the destroy method to delete a user by their imei
    def destroy(self, request, *args, **kwargs):
        imei = request.query_params.get("imei")
        if imei is not None:
            device = Device.objects.filter(imei=imei).first()
            if device is not None:
                # If the user exists, we delete them
                self.perform_destroy(device)
                return Response(status=status.HTTP_204_NO_CONTENT)

        # If the imei does not exist or the user does not exist, we return an error
        return Response(status=status.HTTP_404_NOT_FOUND)

from collections import namedtuple

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Device, UserDevice, CustomUser
from .serializers import (
    DeviceSerializer,
    UserDeviceSerializer,
    UserPhoneDeviceSerializer
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

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a device instance by its primary key (pk)."""
        pk = kwargs.get('pk')
        if pk is not None:
            device = Device.objects.filter(pk=pk).first()
            if device is not None:
                serializer = self.get_serializer(device)
                return Response(serializer.data)

        # If the pk does not exist or the device does not exist, we return an error
        return Response(status=status.HTTP_404_NOT_FOUND)

    def __filter_queryset_by_tracking_alarms(self, request: Request):
        """
        Filters the queryset based on the 'is_tracking_alarms' request parameter.
        """
        param: str = request.query_params.get(
            IS_TRACKING_ALARMS_PARAM.param, IS_TRACKING_ALARMS_PARAM.default_value
        )
        is_tracking_alarms: bool = param.lower() == IS_TRACKING_ALARMS_PARAM.true_value
        self.queryset = self.queryset.filter(is_tracking_alarms=is_tracking_alarms)

    def list(self, request: Request, *args, **kwargs):
        """
        This method is used to retrieve the query for this endpoint.
        Filters the devices based on the 'is_tracking', 'is_tracking_alarms'
        and 'is_tracking_locations' request parameters.
        """
        tracking_param: str = request.query_params.get(
            IS_TRACKING_ALARMS_PARAM.param, None
        )
        if tracking_param is not None:
            self.__filter_queryset_by_tracking_alarms(request)
        return super().list(request, *args, **kwargs)

    def __get_data_from_request(self, request: Request) -> dict:
        """Return data from device in a dict."""
        return {
            "user_name": request.data.get("user_name"),
            "license_number": request.data.get("license_number"),
            "vin": request.data.get("vin"),
            "car_owner": request.data.get("car_owner"),
            "is_tracking_alarms": request.data.get("is_tracking_alarms") or False,
            "last_time_tracked": request.data.get("last_time_tracked") or 0,
        }

    def create(self, request: Request, *args, **kwargs):
        """
        Creates a new device or updates an existing one based on the 'imei' request parameter.
        """
        imei = request.data.get("imei")
        if imei is not None:
            data = self.__get_data_from_request(request)
            device, _ = Device.objects.update_or_create(imei=imei, defaults=data)
            serializer = self.get_serializer(device)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If the imei does not exist, we create a new user
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        """
        Updates the data of an existing device based on the 'imei' request parameter.
        """
        imei = request.data.get("imei")
        if imei is not None:
            data = self.__get_data_from_request(request)
            device, _ = Device.objects.update_or_create(imei=imei, defaults=data)
            serializer = self.get_serializer(device)
            return Response(serializer.data, status=status.HTTP_200_OK)  # Retorna 200 OK

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

class UserPhoneDeviceList(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for read-only operations on UserDevice instances.

    This viewset uses the UserPhoneDeviceSerializer and includes a custom
    get_queryset method to optionally filter the UserDevices by their IMEI.
    """
    serializer_class = UserPhoneDeviceSerializer

    def get_queryset(self):
        """
        Retrieves the queryset of UserDevice instances for this viewset.

        The queryset can be optionally filtered to include only UserDevices
        with a specific IMEI, if an 'imei' keyword argument is included in the URL.

        Returns:
            - QuerySet: The queryset of UserDevice instances.
        """
        imei = self.kwargs.get('imei', None)
        if imei is not None:
            return UserDevice.objects.filter(device__imei=imei)
        return UserDevice.objects.none()

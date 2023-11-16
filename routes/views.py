from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.response import Response

from users.models import CustomUser
from .filters import RouteFilter
from .models import Route, UserRoute
from .serializers import RouteSerializer, UserRouteSerializer


class UserDeviceReadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing the devices associated with a user.
    The retrieve method has been overridden to return only the IMEIs
    of the devices associated with the user specified by the UUID.
    """

    queryset = UserRoute.objects.all()
    serializer_class = UserRouteSerializer

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
        user_routes = UserRoute.objects.filter(user=user)

        if not user_routes.exists():
            return Response([])

        routes = [user_route.route for user_route in user_routes]
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)


class ReadOnlyRouteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing routes.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RouteFilter

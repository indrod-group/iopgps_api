from typing import List, Optional
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets

from users.models import CustomUser
from .filters import RouteFilter
from .models import Route, UserRoute
from .serializers import RouteSerializer


class UserRouteReadAndCreate(
    viewsets.ReadOnlyModelViewSet,
    viewsets.mixins.CreateModelMixin
):
    serializer_class = RouteSerializer

    def get_queryset(self):
        """
        This method retrieves the queryset of Tire objects
        for the vehicle specified by the 'pk' parameter in the URL,
        which corresponds to the 'vuid' of the vehicle.
        If the 'vuid' is None or does not exist, it returns an empty queryset.
        """
        uuid: Optional[str] = self.kwargs.get("uuid")
        if uuid is not None:
            user = get_object_or_404(CustomUser, uuid=uuid)
            routes = UserRoute.objects.filter(user=user)
            return [route.route for route in routes]
        return UserRoute.objects.none()



class RouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing routes which includes operations
    like listing, creating, and updating routes,
    as well as fetching routing data from Geoapify based on the route's positions.
    """

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RouteFilter

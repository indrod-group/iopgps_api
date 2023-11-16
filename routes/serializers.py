from rest_framework import serializers
from .models import Position, Route, RoutePosition, UserRoute


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Position model.
    This serializer includes the 'id', 'name',
    'lat', and 'lng' fields from the Position model.
    """

    class Meta:
        model = Position
        fields = ["id", "name", "lat", "lng"]


class RoutePositionSerializer(serializers.ModelSerializer):
    """
    Serializer for the RoutePosition model.
    This serializer includes the 'id', 'position', 'order', 'distance',
    and 'estimated_time' fields from the RoutePosition model.
    """

    position = PositionSerializer()

    class Meta:
        model = RoutePosition
        fields = ["id", "position", "order", "distance", "estimated_time"]


class RouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.
    This serializer includes the 'id', 'name', and 'positions' fields from the Route model.
    """

    positions = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ["id", "name", "positions"]

    def get_positions(self, obj):
        """
        Method to get all route positions associated with the route.
        """
        positions = RoutePosition.objects.filter(route=obj)
        return RoutePositionSerializer(positions, many=True).data


class UserRouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserRoute model.
    This serializer includes the 'user' and 'routes' fields from the UserRoute model.
    """

    user = serializers.StringRelatedField()
    routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = UserRoute
        fields = [
            "user",
            "routes",
        ]

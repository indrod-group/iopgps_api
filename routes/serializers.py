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
        fields = [
            "id",
            "name",
            "lat",
            "lng",
        ]


class RoutePositionSerializer(serializers.ModelSerializer):
    """
    Serializer for the RoutePosition model.
    This serializer includes the 'id', 'position', 'order', 'distance',
    and 'estimated_time' fields from the RoutePosition model.
    """

    position = PositionSerializer()

    class Meta:
        model = RoutePosition
        fields = [
            "id",
            "position",
            "order",
            "alias",
        ]

    def validate(self, attrs):
        """
        Check that the order is a positive number and
        that there are no duplicate orders for the same route.
        """
        if attrs["order"] <= 0:
            raise serializers.ValidationError("The order must be a positive number.")

        if RoutePosition.objects.filter(
            route=attrs["route"], order=attrs["order"]
        ).exists():
            raise serializers.ValidationError(
                "The order is already used in this route."
            )

        return attrs


class RouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.
    This serializer includes the 'id', 'name', and 'positions' fields from the Route model.
    """

    positions = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = [
            "id",
            "name",
            "description",
            "positions",
        ]

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

    routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = UserRoute
        fields = [
            "routes",
        ]

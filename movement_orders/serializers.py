from rest_framework import serializers
from .models import (
    Incident,
    MovementOrder,
    ClosureMovementOrder,
    MovementOrderState,
)


class MovementOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementOrder
        fields = "__all__"


class MovementOrderStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementOrderState
        fields = "__all__"


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"


class ClosureMovementOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosureMovementOrder
        fields = "__all__"

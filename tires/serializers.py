from rest_framework import serializers
from vehicles.models import Tire

class TireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tire
        fields = '__all__'

from rest_framework import serializers
from .models import BrokerInfo

class BrokerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerInfo
        fields = '__all__'

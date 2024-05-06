from rest_framework import viewsets
from .models import BrokerInfo
from .serializers import BrokerInfoSerializer

class BrokerInfoViewSet(viewsets.ModelViewSet):
    queryset = BrokerInfo.objects.all()
    serializer_class = BrokerInfoSerializer

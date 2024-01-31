from rest_framework import viewsets
from .models import Mileage
from .serializers import MileageSerializer

class MileageViewSet(viewsets.ModelViewSet):
    queryset = Mileage.objects.all()
    serializer_class = MileageSerializer

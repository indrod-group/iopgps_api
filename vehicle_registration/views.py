from rest_framework import viewsets
from .models import VehicleRegistration
from .serializers import VehicleRegistrationSerializer

class VehicleRegistrationViewSet(viewsets.ModelViewSet):
    queryset = VehicleRegistration.objects.all()
    serializer_class = VehicleRegistrationSerializer

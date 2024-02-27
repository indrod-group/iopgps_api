from typing import Optional
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from users.models import CustomUser

from .models import License
from .serializers import LicenseSerializer

class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer

class UserLicenseReadAndCreate(
    viewsets.ReadOnlyModelViewSet,
    viewsets.mixins.CreateModelMixin
):
    serializer_class = LicenseSerializer

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
            return License.objects.filter(driver=user)
        return License.objects.none()

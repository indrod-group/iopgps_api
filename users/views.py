from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from rest_framework.request import Request

from .models import CustomUser, PhoneNumber
from .serializers import (
    ChangePasswordSerializer,
    CustomUserSerializer,
    CustomUserTreeSerializer,
    PhoneNumberSerializer
)


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing CustomUser instances.
    """

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email", "user__username"]


class CustomUserTreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing a tree of CustomUser instances.
    """
    serializer_class = CustomUserTreeSerializer

    def get_queryset(self):
        """
        Overwrite the get_queryset method to return only the user being retrieved.
        """
        uuid = self.kwargs.get('pk')
        return CustomUser.objects.filter(uuid=uuid)

    def retrieve(self, request, *args, **kwargs):
        """
        Overwrite the retrieve method to use the CustomUserTreeSerializer.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ChangePasswordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    A viewset for changing a user's password.
    """

    serializer_class = ChangePasswordSerializer
    queryset = CustomUser.objects.all()

    def update(self, request: Request, *args, **kwargs):
        """
        Updates the user's password.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # pylint: disable=protected-access
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        """
        Overwrites the partial_update method to prevent partial updates.
        """
        raise NotImplementedError("Partial update operation is not allowed.")

class PhoneNumberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows phone numbers to be viewed or edited.
    """
    serializer_class = PhoneNumberSerializer

    def get_queryset(self):
        """
        Overwrite the get_queryset method to return only
        the phone numbers of the user being retrieved.
        """
        uuid = self.kwargs.get('pk')
        return PhoneNumber.objects.filter(user__uuid=uuid)

    def perform_create(self, serializer):
        """
        Overwrite the perform_create method to set the user
        of the phone number being created.
        """
        uuid = self.kwargs.get('pk')
        user = CustomUser.objects.get(uuid=uuid)
        serializer.save(user=user)

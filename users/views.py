from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from rest_framework.request import Request

from .models import CustomUser
from .serializers import ChangePasswordSerializer, CustomUserSerializer


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing CustomUser instances.
    """

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email"]


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

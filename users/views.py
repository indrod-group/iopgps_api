from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminUser
from .models import CustomUser, PhoneNumber, Role
from .serializers import (
    ChangePasswordSerializer,
    CustomUserSerializer,
    CustomUserTreeSerializer,
    PhoneNumberSerializer,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing CustomUser instances. This ViewSet provides
    standard actions for creating, listing, updating, and deleting users, in addition to
    custom actions for updating the user's photo.
    """

    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email", "user__username"]

    def get_queryset(self):
        """
        Overrides the `get_queryset` method to return users based on the user
        making the request. In this case, users that match
        the authenticated user will be filtered.
        """
        user = self.request.user
        return CustomUser.objects.filter(user=user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAdminUser, IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Overrides the `create` method to allow the creation of a new user and its
        corresponding CustomUser, including all necessary fields and role handling.
        """
        user_data: dict = request.data
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )

        # It is assumed that roles come as a list of role names.
        roles = Role.objects.filter(name__in=user_data.get("roles", []))

        custom_user = CustomUser.objects.create(
            user=user,
            id_card=user_data.get("id_card", ""),
            birth_date=user_data.get("birth_date"),
            marital_status=user_data.get("marital_status"),
            education_level=user_data.get("education_level"),
            home_address=user_data.get("home_address"),
            # Add other fields as necessary.
        )
        custom_user.roles.set(roles)

        # Implement logic to handle additional fields like parent_accounts if necessary.

        return Response({"status": "user created"}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Overrides the `update` method to allow the update of a user and its
        corresponding CustomUser, including all necessary fields.
        """
        custom_user: CustomUser = self.get_object()
        user_data: dict = request.data

        # Restrict updating to Admin or Superuser roles
        requested_roles = user_data.get("roles")
        if requested_roles:
            forbidden_roles = ["Admin", "Superuser"]
            if any(role in requested_roles for role in forbidden_roles):
                return Response(
                    {"error": "Updating to Admin or Superuser roles is not allowed"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Update associated Django user
        user = custom_user.user
        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.save()

        # Update CustomUser fields
        CustomUser.objects.filter(pk=custom_user.pk).update(
            id_card=user_data.get("id_card", custom_user.id_card),
            birth_date=user_data.get("birth_date", custom_user.birth_date),
            marital_status=user_data.get("marital_status", custom_user.marital_status),
            education_level=user_data.get(
                "education_level", custom_user.education_level
            ),
            home_address=user_data.get("home_address", custom_user.home_address),
            # Add or update other fields as necessary.
        )

        # Update roles if they are sent
        if "roles" in user_data:
            roles = Role.objects.filter(name__in=user_data["roles"])
            custom_user.roles.set(roles)

        return Response({"status": "user updated"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def update_photo(self, request, pk=None):
        """
        A custom action to update a user's photo.
        The photo file must be sent in the body of the request.
        """
        custom_user = self.get_object()
        custom_user.photo = request.data.get("photo")
        custom_user.save()
        return Response({"status": "photo updated"})


class CustomUserTreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing a tree of CustomUser instances.
    """

    serializer_class = CustomUserTreeSerializer

    def get_queryset(self):
        """
        Overwrite the get_queryset method to return only the user being retrieved.
        """
        uuid = self.kwargs.get("pk")
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
        uuid = self.kwargs.get("pk")
        return PhoneNumber.objects.filter(user__uuid=uuid)

    def perform_create(self, serializer):
        """
        Overwrite the perform_create method to set the user
        of the phone number being created.
        """
        uuid = self.kwargs.get("pk")
        user = CustomUser.objects.get(uuid=uuid)
        serializer.save(user=user)

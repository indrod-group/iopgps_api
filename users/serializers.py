from collections import OrderedDict
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import CustomUser


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    Takes the uuid, the old password and two instances of the new password as input.
    Validates that the uuid exists, the new passwords match and that
    the old password is correct before updating the user's password.
    """

    uuid = serializers.UUIDField(
        required=True,
        write_only=True,
        help_text=_("UUID of the user whose password will be changed.")
    )
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text=_("Current password of the user.")
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text=_("New password to be set for the user.")
    )
    confirm_new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text=_("Confirmation of the new password.")
    )

    def validate_uuid(self, value):
        """
        Validates that the uuid exists in the database.
        """
        if not CustomUser.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("The uuid does not exist.")
        return value

    def validate_old_password(self, value):
        """
        Validates that the old password is not empty.
        """
        if not value:
            raise serializers.ValidationError("The old password cannot be empty.")
        return value

    def validate_new_password(self, value):
        """
        Validates that the new password is not empty and meets length requirements.
        """
        password_validation.validate_password(value)
        return value

    def validate_confirm_new_password(self, value):
        """
        Validates that the new password is not empty and meets length requirements.
        """
        password_validation.validate_password(value)
        return value

    def validate(self, attrs: OrderedDict):
        """
        Validates that the new passwords match.
        """
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError("The new passwords do not match.")
        return attrs

    def update(self, instance: CustomUser, validated_data: OrderedDict):
        """
        Checks that the old password is correct before updating the user's password.
        """
        user = instance.user
        if not user.check_password(validated_data.get("old_password")):
            raise serializers.ValidationError("The old password is incorrect.")
        user.set_password(validated_data.get("new_password"))
        user.save()
        return instance

    def partial_update(self, instance, validated_data):
        """
        Overwrites the partial_update method to prevent partial updates.
        """
        raise NotImplementedError("Partial update operation is not allowed.")

    def create(self, validated_data):
        """
        Overwrites the create method to prevent creations.
        """
        raise NotImplementedError("Create operation is not allowed.")

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model. Includes all fields except
    for 'uuid', 'is_staff', and 'is_active', which are read-only.
    """
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "uuid",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "id_card",
            "role",
        )
        read_only_fields = ("uuid", "is_staff", "is_active")

    def get_email(self, obj: CustomUser):
        return obj.user.email

    def get_first_name(self, obj: CustomUser):
        return obj.user.first_name or "Usuario"

    def get_last_name(self, obj: CustomUser):
        return obj.user.last_name or ""

    def get_is_active(self, obj: CustomUser):
        return obj.user.is_active or False

    def get_is_staff(self, obj: CustomUser):
        return obj.user.is_staff or False

    def create(self, validated_data):
        """
        Overwrites the create method to prevent creations.
        """
        raise serializers.ValidationError("Create operation is not allowed.")

    def update(self, instance, validated_data):
        """
        Overwrites the update method to prevent updates.
        """
        raise serializers.ValidationError("Update operation is not allowed.")

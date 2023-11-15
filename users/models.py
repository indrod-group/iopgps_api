import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class Roles(models.TextChoices):
    """
    User role choices
    """
    SUPERUSER = "Superuser", "SuperUser"
    ADMIN = "Admin", "Administrator"
    DRIVER = "Driver", "Driver"

class CustomUser(models.Model):
    """
    Custom user model that extends the base User model and adds additional fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    id_card = models.CharField(
        max_length=13, blank=True, null=True, help_text=_("User's ID card number")
    )
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.DRIVER.value,
        help_text=_("User's role in the system"),
    )

    def __str__(self) -> str:
        return f"{self.user}"

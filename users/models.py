import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Roles(models.TextChoices):
    """
    User role choices, each with a specific set of responsibilities:

    - SuperUser: Has all permissions and can perform any action in the system.
    - Admin: Has permissions to manage users, assign roles, and oversee general operations.
    - Driver: Responsible for driving vehicles according to assigned movement orders.
    - TransportManager: In charge of logistics and transportation planning.
        Can assign movement orders to drivers.
    - Secretary: Performs administrative and office tasks,
        such as scheduling appointments or maintaining records.
    - Dispatcher: Responsible for coordinating and dispatching vehicles,
        drivers, or loads to appropriate destinations.
    - Maintenance: In charge of vehicle repair and maintenance.
    """

    SUPERUSER = "Superuser", "SuperUser"
    ADMIN = "Admin", "Administrator"
    DRIVER = "Driver", "Driver"
    TRANSPORT_MANAGER = "TransportManager", "Transport Manager"
    SECRETARY = "Secretary", "Secretary"
    DISPATCHER = "Dispatcher", "Dispatcher"
    MAINTENANCE = "Maintenance", "Maintenance"


class Role(models.Model):
    """
    Model to represent user roles.
    """

    name = models.CharField(
        max_length=32,
        choices=Roles.choices,
        unique=True,
        help_text=_("User's role")
    )

    def __str__(self) -> str:
        return f"{self.name}"

class CustomUser(models.Model):
    """
    Custom user model that extends the base User model and adds additional fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, db_index=True
    )
    id_card = models.CharField(
        max_length=13, blank=True, null=True, help_text=_("User's ID card number")
    )
    roles = models.ManyToManyField(Role, help_text=_("User's roles in the system"))
    parent_accounts = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name='child_accounts'
    )

    def __str__(self) -> str:
        return f"{self.user}"

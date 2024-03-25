import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .utils import path_and_rename


class Roles(models.TextChoices):
    """
    User role choices, each with a specific set of responsibilities:

    - SuperUser: Has all permissions and can perform any action in the system.
    - Admin: Has permissions to manage users, assign roles,
        and oversee general operations.
    - Driver: Responsible for driving vehicles according
        to assigned movement orders.
    - TransportManager: In charge of logistics and transportation planning.
        Can assign movement orders to drivers.
    - Secretary: Performs administrative and office tasks,
        such as scheduling appointments or maintaining records.
    - Dispatcher: Responsible for coordinating and dispatching vehicles,
        drivers, or loads to appropriate destinations.
    - Maintenance: In charge of vehicle repair and maintenance.
    - Supervisor: Oversees the work of others and ensures that tasks are
        completed correctly and on time.
    - Mechanic: Responsible for repairing and maintaining vehicles.
    - Logistics: In charge of managing the flow of goods
        and resources in a company.
    """

    SUPERUSER = "Superuser", "SuperUser"
    ADMIN = "Admin", "Administrator"
    DRIVER = "Driver", "Driver"
    TRANSPORT_MANAGER = "TransportManager", "Transport Manager"
    SECRETARY = "Secretary", "Secretary"
    DISPATCHER = "Dispatcher", "Dispatcher"
    MAINTENANCE = "Maintenance", "Maintenance"
    SUPERVISOR = "Supervisor", "Supervisor"
    MECHANIC = "Mechanic", "Mechanic"
    LOGISTICS = "Logistics", "Logistics"


class Role(models.Model):
    """
    Model to represent user roles.
    """

    name = models.CharField(
        max_length=32, choices=Roles.choices, unique=True, help_text=_("User's role")
    )

    def __str__(self) -> str:
        return f"{self.name}"


class MaritalStatus(models.TextChoices):
    """
    Enumeration class to represent different marital statuses.
    """

    MARRIED = "Married"
    DIVORCED = "Divorced"
    SINGLE = "Single"
    FREE_UNION = "Free Union"
    WIDOWED = "Widowed"


class EducationLevel(models.TextChoices):
    """
    Enumeration class to represent different education levels.
    """

    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    BACHELOR = "Bachelor"
    UNIVERSITY = "University"


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
        "self", blank=True, symmetrical=False, related_name="child_accounts"
    )
    birth_date = models.DateField(
        null=True, blank=True, help_text=_("User's birth date")
    )
    marital_status = models.CharField(
        max_length=32,
        choices=MaritalStatus.choices,
        default=MaritalStatus.SINGLE,
        help_text=_("User's marital status"),
    )
    education_level = models.CharField(
        max_length=32,
        choices=EducationLevel.choices,
        default=EducationLevel.PRIMARY,
        help_text=_("User's education level"),
    )
    home_address = models.CharField(
        max_length=256, blank=True, null=True, help_text=_("User's home address")
    )
    photo = models.ImageField(
        upload_to=path_and_rename, null=True, blank=True, help_text=_("User's photo")
    )

    def __str__(self) -> str:
        return f"{self.user}"


class PhoneNumber(models.Model):
    """
    Model to represent a user's phone numbers.
    Each instance of this model represents a phone number that is associated with a user.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text=_("The user to whom this phone number belongs"),
    )
    phone_number = PhoneNumberField(
        blank=True, null=True, help_text=_("User's phone number")
    )

    def __str__(self) -> str:
        return f"{self.phone_number}"

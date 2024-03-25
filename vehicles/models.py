import uuid

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from devices.models import Device
from users.models import CustomUser
from vehicles.utils import path_and_rename

from .enums import (
    Colors,
    FuelType,
    VehicleChoices,
    VehicleCondition,
    TirePosition,
)
from .validators import (
    validate_manufacture_year,
    validate_battery_code,
    validate_dot_code,
    validate_vehicle_plate,
)


class VehicleType(models.Model):
    """
    Model representing a type of vehicle with various attributes.
    """

    year = models.PositiveSmallIntegerField(
        validators=[validate_manufacture_year], help_text=_("Year of the vehicle")
    )
    brand = models.CharField(max_length=255, help_text=_("Brand of the vehicle"))
    model = models.CharField(max_length=255, help_text=_("Model of the vehicle"))
    version = models.CharField(
        max_length=255, blank=True, help_text=_("Version of the vehicle")
    )
    fuel_type = models.CharField(
        max_length=31,
        default=FuelType.GASOLINE,
        choices=FuelType.choices,
        help_text=_("Type of fuel used by the vehicle"),
    )
    fuel_value = models.DecimalField(
        default="0.0",
        blank=True,
        max_digits=6,
        decimal_places=4,
        help_text=_("Fuel value for the vehicle"),
    )
    engine_displacement = models.DecimalField(
        default="0.0",
        blank=True,
        max_digits=5,
        decimal_places=3,
        help_text=_("Engine displacement of the vehicle"),
    )
    vehicle_type = models.CharField(
        default=VehicleChoices.CAR,
        max_length=31,
        choices=VehicleChoices.choices,
        help_text=_("Type of the vehicle"),
    )
    city_mileage = models.DecimalField(
        default="0.0",
        blank=True,
        max_digits=5,
        decimal_places=2,
        help_text=_("City fuel efficiency"),
    )
    highway_mileage = models.DecimalField(
        default="0.0",
        blank=True,
        max_digits=5,
        decimal_places=2,
        help_text=_("Highway fuel efficiency"),
    )
    mixed_mileage = models.DecimalField(
        default="0.0",
        blank=True,
        max_digits=5,
        decimal_places=2,
        help_text=_("Mixed fuel efficiency"),
    )

    class Meta:
        verbose_name = _("Vehicle Type")
        verbose_name_plural = _("Vehicle Types")

    def __str__(self) -> str:
        return f"{self.brand} {self.model} ({self.year})"


class Vehicle(models.Model):
    """
    Model representing a vehicle with various attributes.
    """

    vuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        db_index=True,
        help_text=_("UUID of the vehicle"),
    )
    vehicle_type = models.ForeignKey(
        VehicleType, on_delete=models.PROTECT, help_text=_("Type of the vehicle")
    )
    device = models.OneToOneField(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("Device installed in the vehicle"),
    )
    color = models.CharField(
        max_length=6,
        default=Colors.WHITE,
        validators=[RegexValidator(r'^[0-9A-Fa-f]{6}$')],
        help_text=_("Color of the vehicle in hexadecimal"),
    )
    chassis = models.CharField(
        blank=True, max_length=255, help_text=_("Chassis number of the vehicle")
    )
    plate = models.CharField(
        blank=True,
        max_length=10,
        validators=[validate_vehicle_plate],
        help_text=_("Vehicle plate number"),
    )
    tonnage = models.DecimalField(
        blank=True,
        max_digits=5,
        decimal_places=2,
        help_text=_("Tonnage of the vehicle"),
    )
    vin = models.CharField(
        blank=True, max_length=31, help_text=_("Vehicle Identification Number (VIN)")
    )
    front_photo = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Front photo of the vehicle"),
    )
    left_side_photo = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Left side photo of the vehicle"),
    )
    right_side_photo = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Right side photo of the vehicle"),
    )
    rear_photo = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Rear photo of the vehicle"),
    )
    heavy_transport_permit = models.FileField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Heavy transport permit of the vehicle"),
    )

    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def __str__(self) -> str:
        return f"Vehicle #{self.vuid}: - {self.vehicle_type}"


class VehicleStatus(models.Model):
    """
    Model representing the condition of a vehicle.
    """

    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    condition = models.CharField(
        max_length=31,
        default=VehicleCondition.OPERABLE,
        choices=VehicleCondition.choices,
        help_text=_("Condition of the vehicle"),
    )
    status_updated_at = models.PositiveBigIntegerField(
        help_text=_("The date the status was updated")
    )

    class Meta:
        verbose_name = _("Vehicle Condition")
        verbose_name_plural = _("Vehicle Conditions")

    def __str__(self) -> str:
        return f"{self.condition}-{self.status_updated_at}"


class UserVehicle(models.Model):
    """
    Model representing a relationship between a user and a vehicle.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, help_text=_("User who owns the vehicle")
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, help_text=_("Vehicle owned by the user")
    )

    class Meta:
        verbose_name = _("User Vehicle")
        verbose_name_plural = _("User Vehicles")

    def __str__(self) -> str:
        return f"User - {self.user}, Vehicle - {self.vehicle}"


class TrackableItem(models.Model):
    """
    Abstract base model with common fields for Tire and Battery.
    """

    registration_date = models.PositiveBigIntegerField(
        help_text=_("The date the item was registered")
    )
    in_use = models.BooleanField(
        default=True, help_text=_("Whether the item is currently in use")
    )
    location = models.CharField(
        max_length=255, blank=True, help_text=_("Where the item is currently located")
    )
    notes = models.TextField(
        blank=True, help_text=_("Additional information or observations about the item")
    )
    manufacturer = models.CharField(
        max_length=255, blank=True, help_text=_("The manufacturer of the item")
    )
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The cost of the item"),
    )

    class Meta:
        abstract = True


class Tire(TrackableItem):
    """
    Represents a tire of a vehicle.

    Attributes:
        - vehicle (Vehicle): The vehicle to which the tire belongs.
        - manufacturing_code (str): The manufacturing code of the tire.
        - position_relative_to_vehicle (str): The position of the tire relative to the vehicle.
    """

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="tires",
        help_text=_("The vehicle to which the tire belongs."),
    )
    manufacturing_code = models.CharField(
        _("Manufacturing code"),
        max_length=18,
        help_text=_("The manufacturing code of the tire."),
        validators=[
            validate_dot_code,
        ],
    )
    position_relative_to_vehicle = models.CharField(
        _("Position relative to vehicle"),
        max_length=50,
        choices=TirePosition.choices,
        help_text=_("The position of the tire relative to the vehicle."),
    )

    def __str__(self) -> str:
        return f"Tire {self.position_relative_to_vehicle} of {self.vehicle}"


class Battery(TrackableItem):
    """
    Represents a battery of a vehicle.

    Attributes:
        - vehicle (Vehicle): The vehicle to which the battery belongs.
        - manufacturing_code (str): The manufacturing code of the battery.
    """

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="batteries",
        help_text=_("The vehicle to which the battery belongs."),
    )
    manufacturing_code = models.CharField(
        _("Manufacturing code"),
        max_length=50,
        help_text=_("The manufacturing code of the battery."),
        validators=[
            validate_battery_code,
        ],
    )

    def __str__(self) -> str:
        return f"Battery of {self.vehicle}"

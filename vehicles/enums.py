from django.db import models
from django.utils.translation import gettext_lazy as _


class VehicleChoices(models.TextChoices):
    CAR = "car", _("Car")
    TRUCK = "truck", _("Truck")
    MOTORCYCLE = "motorcycle", _("Motorcycle")
    VAN = "van", _("Van")
    BUS = "bus", _("Bus")
    BICYCLE = "bicycle", _("Bicycle")

class FuelType(models.TextChoices):
    """
    Enumeration of different types of fuels.
    """
    GASOLINE = "Gasoline", "Gasoline"
    DIESEL = "Diesel", "Diesel"
    GAS = "Gas", "Gas"
    ELECTRIC = "Electric", "Electric"

class VehicleCondition(models.TextChoices):
    """
    Enumeration of different vehicle conditions.
    """
    OPERABLE = "Operable", "Operable"
    INOPERABLE = "Inoperable", "Inoperable"
    UNDER_MAINTENANCE = "Under Maintenance", "Under Maintenance"

class TirePosition(models.TextChoices):
    """
    Enumeration of different tire positions.
    """
    FRONT_RIGHT = "Front Right", "Front Right"
    REAR_RIGHT = "Rear Right", "Rear Right"
    REAR_RIGHT_OUTER = "Rear Right Outer", "Rear Right Outer"
    REAR_RIGHT_INNER = "Rear Right Inner", "Rear Right Inner"
    FRONT_LEFT = "Front Left", "Front Left"
    REAR_LEFT = "Rear Left", "Rear Left"
    REAR_LEFT_OUTER = "Rear Left Outer", "Rear Left Outer"
    REAR_LEFT_INNER = "Rear Left Inner", "Rear Left Inner"
    SPARE = "Spare", "Spare"

class OdometerUnit(models.TextChoices):
    """
    Enumeration of different units for measuring mileage.
    """
    KILOMETERS = "km", "km"
    MILES = "mi", "mi"
    DAYS = "days", "days"

class Colors(models.TextChoices):
    """Colors choices for vehicles."""
    WHITE = 'FFFFFF', _('White')
    BLACK = '000000', _('Black')
    RED = 'FF0000', _('Red')
    BLUE = '0000FF', _('Blue')
    GREEN = '008000', _('Green')
    YELLOW = 'FFFF00', _('Yellow')
    ORANGE = 'FFA500', _('Orange')
    PURPLE = '800080', _('Purple')
    PINK = 'FFC0CB', _('Pink')
    BROWN = 'A52A2A', _('Brown')
    GRAY = '808080', _('Gray')

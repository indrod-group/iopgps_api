from django.db import models
from django.utils.translation import gettext_lazy as _


class DistanceUnit(models.TextChoices):
    """
    Enumeration of the different units for measuring distance
    according to the International System of Units.
    """

    METERS = "m", _("Meters")
    KILOMETERS = "km", _("Kilometers")
    MILES = "mi", _("Miles")
    NAUTICAL_MILES = "nmi", _("Nautical Miles")


class TimeUnits(models.TextChoices):
    """
    Enumeration of the different units for measuring time
    according to the International System of Units.
    """

    MINUTES = "min", _("Minutes")
    HOURS = "h", _("Hours")
    DAYS = "d", _("Days")
    WEEKS = "w", _("Weeks")
    MONTHS = "m", _("Months")
    YEARS = "y", _("Years")


class Tasks(models.TextChoices):
    """
    Enumeration of the maintenance tasks that can be performed
    on a vehicle within the maintenance manual.
    """

    INSPECT = "I", _("Inspect and correct or replace if necessary.")
    ADJUST = "A", _("Adjust.")
    REPLACE = "R", _("Replace or change.")
    TORQUE = "T", _("Tighten to specified torque.")
    LUBRICATE = "L", _("Lubricate and/or grease.")
    CLEAN = "C", _("Clean.")
    CHECK = "CK", _("Check.")
    TEST = "TS", _("Test.")
    SERVICE = "SV", _("Service.")

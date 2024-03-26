from django.db import models
from django.utils.translation import gettext_lazy as _

class OdometerUnits(models.TextChoices):
    """
    Enumeration of the different units for measuring distance
    according to the International System of Units.
    """

    METERS = "m", _("Meters")
    KILOMETERS = "km", _("Kilometers")
    MILES = "mi", _("Miles")
    NAUTICAL_MILES = "nmi", _("Nautical Miles")
    MINUTES = "min", _("Minutes")
    HOURS = "h", _("Hours")
    DAYS = "d", _("Days")
    WEEKS = "w", _("Weeks")
    MONTHS = "mo", _("Months")
    YEARS = "y", _("Years")

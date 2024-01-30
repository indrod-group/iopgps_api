from django.db import models
from django.utils.translation import gettext_lazy as _

class OdometerUnit(models.TextChoices):
    """
    Enumeration of the different units for measuring mileage.
    """
    KILOMETERS = 'km', _('Kilometers')
    MILES = 'mi', _('Miles')
    HOURS = "hours", _('Hours')
    DAYS = 'days', _('Days')
    WEEKS = 'weeks', _('Weeks')
    MONTHS = 'months', _('Months')

class Tasks(models.TextChoices):
    """
    Enumeration of the maintenance tasks that can be performed
    on a vehicle within the maintenance manual.
    """
    INSPECT = 'I', _('Inspect and correct or replace if necessary.')
    ADJUST = 'A', _('Adjust.')
    REPLACE = 'R', _('Replace or change.')
    TORQUE = 'T', _('Tighten to specified torque.')
    LUBRICATE = 'L', _('Lubricate and/or grease.')

from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import OdometerUnits
from vehicles.models import Vehicle

class Mileage(models.Model):
    """
    Represents the odometer of a vehicle.
    """
    vehicle = models.ForeignKey(
        Vehicle,
        related_name='mileage_log',
        on_delete=models.CASCADE,
        help_text=_("The vehicle to which the odometer belongs.")
    )
    mileage = models.DecimalField(
        _('Mileage'),
        max_digits=10,
        decimal_places=2,
        blank=False,
        help_text=_("The mileage traveled by the vehicle.")
    )
    unit = models.CharField(
        _('Unit'),
        max_length=10,
        blank=False,
        choices=OdometerUnits.choices,
        help_text=_("The unit of measure of the mileage.")
    )
    unix_time_registered = models.PositiveBigIntegerField(
        _('Date'),
        blank=False,
        help_text=_("The date when the mileage was registered.")
    )

    class Meta:
        verbose_name = _("Mileage")
        verbose_name_plural = _("Mileages")

    def __str__(self):
        return f'{self.vehicle}: {self.mileage} {self.unit} - {self.unix_time_registered}'

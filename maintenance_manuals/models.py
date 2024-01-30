from django.db import models
from django.utils.translation import gettext_lazy as _

from vehicles.models import Vehicle

from .enums import (
    Tasks,
    OdometerUnit
)

class MaintenanceManual(models.Model):
    """
    Represents a maintenance manual for a vehicle.

    Attributes:
        - vehicle (Vehicle): The vehicle to which the maintenance sheet belongs.
        - operations (list[Operation]): The maintenance operations to be performed on the vehicle.
    """
    vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.PROTECT,
        help_text=_("The vehicle to which the maintenance manual belongs.")
    )
    start_date = models.DateField(
        blank=False,
        help_text=_("The start date of the maintenance cycle.")
    )
    advance_alerts_mileage = models.DecimalField(
        _('Advance alerts'),
        max_digits=10,
        decimal_places=2,
        blank=False,
        help_text=_("Using this value it is possible to anticipate maintenance in advance.")
    )
    advance_alerts_days = models.DecimalField(
        _('Advance alerts'),
        max_digits=10,
        decimal_places=2,
        blank=False,
        help_text=_("Using this value it is possible to anticipate maintenance in advance.")
    )
    minimum_frequency = models.DecimalField(
        _('Minimum frequency'),
        max_digits=10,
        decimal_places=2,
        blank=False,
        help_text=_("The minimum mileage/time at which operations should be performed.")
    )
    end_of_cycle = models.DecimalField(
        _('End of maintenance cycle'),
        max_digits=10,
        decimal_places=2,
        blank=False,
        help_text=_("The mileage/time limit that marks the end of each maintenance cycle.")
    )
    unit = models.CharField(
        _('Unit'),
        max_length=10,
        blank=False,
        choices=OdometerUnit.choices,
        help_text=_("The unit of measure of the mileage.")
    )

    class Meta:
        verbose_name = _("Maintenance manual")
        verbose_name_plural = _("Maintenance manuals")

    def __str__(self):
        return (
            f'{self.vehicle}'
            f' - Minimum frequency: {self.minimum_frequency} {self.unit}'
            f' - End of cycle: {self.end_of_cycle} {self.unit}'
        )


class MaintenanceOperation(models.Model):
    """
    Represents a maintenance operation.
    """
    maintenance_manual = models.ForeignKey(
        MaintenanceManual,
        on_delete=models.PROTECT,
        related_name='vehicle_systems',
        help_text=_("Maintenance manual to which this system belongs.")
    )
    system =  models.CharField(
        _('System'),
        max_length=50,
        blank=False,
        help_text=_("The vehicle's system.")
    )
    subsystem = models.CharField(
        _('Sub-system'),
        max_length=50,
        blank=False,
        help_text=_("Subsystem of the vehicle's main system.")
    )
    task = models.CharField(
        _('Task'),
        max_length=50,
        blank=False,
        choices=Tasks.choices,
        help_text=_("The task to be performed in the operation.")
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_('Description of the task to be performed')
    )
    frequency = models.DecimalField(
        _('Frequency'),
        max_digits=10,
        decimal_places=2,
        blank=False,
        help_text=_("The mileage/time at which the operation should be performed.")
    )
    frequency_days = models.IntegerField(
        _('Frequency in days'),
        blank=True,
        null=True,
        help_text=_("The frequency at which the operation should be performed, in days.")
    )
    help_me = models.TextField(
        _('Help me'),
        blank=True,
        help_text=_('Additional information to help perform the maintenance task')
    )

    class Meta:
        verbose_name = _("Maintenance operation")
        verbose_name_plural = _("Maintenance operations")

    def __str__(self):
        return f'{self.task} every {self.frequency} {self.maintenance_manual.unit}'

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from vehicles.models import Vehicle

from .enums import (
    Tasks,
)

DISTANCE_VALIDATOR = r"(\d+(([hkn]{0,1}|da)m(i){0,1})|\-)"
TIME_VALIDATOR = r"(\d{1,4}(h|d|w|m|y)|\-)"
FRECUENCY_VALIDATOR = rf"^{DISTANCE_VALIDATOR},{DISTANCE_VALIDATOR},{TIME_VALIDATOR}$"


class MaintenanceManual(models.Model):
    """
    Represents a maintenance manual for a vehicle.
    """

    vehicle = models.ForeignKey(
        Vehicle,
        related_name="vehicle_manual",
        on_delete=models.PROTECT,
        help_text=_("The vehicle to which the maintenance manual belongs."),
    )
    start_date = models.DateField(
        blank=False, help_text=_("The start date of the maintenance cycle.")
    )
    advance_alerts = models.CharField(
        _("Advance alerts"),
        default="-,-,-",
        max_length=64,
        validators=[RegexValidator(FRECUENCY_VALIDATOR)],
        blank=False,
        help_text=_(
            "Using this value it is possible to anticipate maintenance in advance."
        ),
    )
    minimum_frequency = models.CharField(
        _("Minimum frequency"),
        default="-,-,-",
        max_length=64,
        blank=False,
        validators=[RegexValidator(FRECUENCY_VALIDATOR)],
        help_text=_(
            "The minimum mileage/time at which operations should be performed."
        ),
    )
    end_of_cycle = models.CharField(
        _("End of maintenance cycle"),
        default="-,-,-",
        max_length=64,
        blank=False,
        validators=[RegexValidator(FRECUENCY_VALIDATOR)],
        help_text=_(
            "The mileage/time limit that marks the end of each maintenance cycle."
        ),
    )
    manual_file = models.FileField(
        upload_to="manuals/",
        null=True,
        blank=True,
        help_text=_("The original maintenance manual document."),
    )

    class Meta:
        verbose_name = _("Maintenance manual")
        verbose_name_plural = _("Maintenance manuals")

    def __str__(self):
        return (
            f"{self.vehicle}"
            f" - Minimum frequency: {self.minimum_frequency}"
            f" - End of cycle: {self.end_of_cycle}"
        )


class MaintenanceOperation(models.Model):
    """
    Represents a maintenance operation.
    """

    maintenance_manual = models.ForeignKey(
        MaintenanceManual,
        on_delete=models.PROTECT,
        related_name="manual_tasks",
        help_text=_("Maintenance manual to which this system belongs."),
    )
    system = models.CharField(
        _("System"), max_length=50, blank=False, help_text=_("The vehicle's system.")
    )
    subsystem = models.CharField(
        _("Sub-system"),
        max_length=50,
        blank=False,
        help_text=_("Subsystem of the vehicle's main system."),
    )
    task = models.CharField(
        _("Task"),
        max_length=50,
        blank=False,
        choices=Tasks.choices,
        help_text=_("The task to be performed in the operation."),
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Description of the task to be performed"),
    )
    frequency = models.CharField(
        _("Frequency"),
        default="-,-,-",
        max_length=64,
        validators=[RegexValidator(FRECUENCY_VALIDATOR)],
        blank=False,
        help_text=_("The mileage at which the operation should be performed."),
    )
    help_me = models.TextField(
        _("Help me"),
        blank=True,
        help_text=_("Additional information to help perform the maintenance task"),
    )

    class Meta:
        verbose_name = _("Maintenance operation")
        verbose_name_plural = _("Maintenance operations")

    def __str__(self):
        return f"{self.task} every {self.frequency}"

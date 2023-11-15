from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from devices.models import Device
from .alarm_codes import AlarmCodes

MAX_DIGITS = 10
MAX_DECIMAL_PLACES = 7


class Coordinates(models.Model):
    """
    Abstract model to represent geographic coordinates.
    """

    lat = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True,
        null=True,
        help_text=_("Latitude of the location.")
    )
    lng = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        blank=True,
        null=True,
        help_text=_("Longitude of the location.")
    )
    time = models.PositiveBigIntegerField(
        help_text=_("Time when the coordinates were recorded.")
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"Coordinates(lat={self.lat}, lng={self.lng}, time={self.time})"

    def __repr__(self) -> str:
        return self.__str__()

class Alarm(Coordinates):
    """
    Model to represent an alarm event. Each alarm is associated with a device and 
    contains information about the geographic coordinates where the alarm occurred, 
    the type of alarm, the course of the device when the alarm occurred, the type of 
    device, the type of position, and the speed of the device when the alarm occurred.
    """

    device = models.ForeignKey(
        Device,
        on_delete=models.PROTECT,
        help_text=_("Device that triggered the alarm."),
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text=_("Geographic address where the alarm occurred."),
    )
    alarm_code = models.CharField(
        max_length=20,
        choices=AlarmCodes.choices,
        default=AlarmCodes.ACCOFF,
        help_text=_("Code representing the type of alarm."),
    )
    alarm_type = models.IntegerField(
        help_text=_("Integer representing the type of alarm."),
    )
    course = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Course of the device when the alarm occurred."),
    )
    device_type = models.IntegerField(
        help_text=_("Integer representing the type of device that triggered the alarm."),
    )
    position_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Type of position data associated with the alarm."),
    )
    speed = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Speed of the device when the alarm occurred."),
    )

    class Meta:
        verbose_name = _("Alarm")
        verbose_name_plural = _("Alarms")

    def __str__(self) -> str:
        return f"Alarm(code={self.alarm_code})"

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser

class ProviderChoices(models.TextChoices):
    """
    Enumeration for satellite tracking providers.
    - WANWAYTECH: Represents the WanWayTech provider.
    - WHATSGPS: Represents the WhatsGPS provider.
    """
    WANWAYTECH = 'WanWayTech', _('WanWayTech')
    WHATSGPS = 'WhatsGPS', _('WhatsGPS')

class Device(models.Model):
    """
    Model representing a device with various attributes like IMEI,
    user name, car owner, license number, VIN,
    and flags indicating if the device is tracking alarms and locations.
    """

    imei = models.CharField(
        _("Device IMEI"),
        max_length=15,
        primary_key=True,
        unique=True,
        help_text=_(
            "The device's International Mobile Equipment Identity (IMEI) number."
        ),
    )
    user_name = models.CharField(
        _("User Name"),
        max_length=255,
        help_text=_("The name of the user associated with the device."),
    )
    car_owner = models.CharField(
        _("Car Owner"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of the car owner. This field can be left blank."),
    )
    license_number = models.CharField(
        _("License Number"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The license number of the car. This field can be left blank."),
    )
    vin = models.CharField(
        _("VIN"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "The Vehicle Identification Number (VIN) of the car. This field can be left blank."
        ),
    )
    is_tracking_alarms = models.BooleanField(
        _("Is Tracking Alarms"),
        default=False,
        help_text=_("A flag indicating if the device is tracking alarms."),
    )
    last_time_tracked = models.PositiveBigIntegerField(
        _("Last Time Tracked"),
        default=0,
        help_text=_("The last time when the device alarms were tracked.")
    )
    provider = models.CharField(
        _("Provider"),
        max_length=50,
        choices=ProviderChoices.choices,
        default=ProviderChoices.WANWAYTECH,
        help_text=_("The provider of the device.")
    )

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")

    def __str__(self) -> str:
        return f"{self.imei} - {self.user_name}"

    def __repr__(self) -> str:
        return (
            f"Device(imei={self.imei}, "
            f"user_name={self.user_name}, "
            f"car_owner={self.car_owner}, "
            f"license_number={self.license_number}, "
            f"vin={self.vin}, "
            f"is_tracking_alarms={self.is_tracking_alarms}, "
            f"last_time_tracked={self.last_time_tracked}, "
            f"provider={self.provider}"
        )

class UserDevice(models.Model):
    """
    Model representing the association between users and devices.
    A user can use multiple devices and a device can be used by multiple users.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "User Device"
        verbose_name_plural = "User Devices"

    def __str__(self) -> str:
        return f"UserDevice(id={self.id})"

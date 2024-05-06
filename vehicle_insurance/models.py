import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from licenses.validators import validate_issue_date, validate_license_validity
from vehicles.models import Vehicle
from vehicles.utils import path_and_rename


class BrokerInfo(models.Model):
    """
    Model representing a vehicle's broker information.
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        db_index=True,
        help_text=_("UUID of the broker info"),
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="broker_infos",
        help_text=_("The vehicle that this broker info belongs to"),
    )
    insurance_document = models.FileField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Insurance document of the vehicle"),
    )
    issue_date = models.DateField(
        validators=[validate_issue_date],
        help_text=_("Issue date of the insurance document"),
    )
    expiry_date = models.DateField(
        validators=[validate_license_validity],
        help_text=_("Expiry date of the insurance document"),
    )
    insurance_company = models.CharField(
        max_length=255, help_text=_("Name of the insurance company")
    )
    broker_name = models.CharField(max_length=255, help_text=_("Name of the broker"))

    class Meta:
        verbose_name = _("Broker Info")
        verbose_name_plural = _("Broker Infos")

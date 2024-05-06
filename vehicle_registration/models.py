import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from licenses.validators import validate_issue_date, validate_license_validity
from vehicles.models import Vehicle
from vehicles.utils import path_and_rename


class VehicleRegistration(models.Model):
    """
    Model representing a vehicle's registration information.
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        db_index=True,
        help_text=_("UUID of the vehicle registration"),
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="registrations",
        help_text=_("The vehicle that this registration belongs to"),
    )
    registration_document = models.FileField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Vehicle registration document"),
    )
    issue_date = models.DateField(
        validators=[validate_issue_date],
        help_text=_("Issue date of the vehicle registration"),
    )
    expiry_date = models.DateField(
        validators=[validate_license_validity],
        help_text=_("Expiry date of the vehicle registration"),
    )

    class Meta:
        verbose_name = _("Vehicle Registration")
        verbose_name_plural = _("Vehicle Registrations")

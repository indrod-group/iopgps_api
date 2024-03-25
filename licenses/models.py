from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser

from .utils import path_and_rename
from .validators import validate_issue_date, validate_license_validity


class LicenseTypes(models.TextChoices):
    """
    License type choices:

    - A: For motorcycles and mopeds.
    - B: For cars.
    - C: For trucks.
    - D: For buses.
    - E: For articulated vehicles.
    """

    A = "A", _("A")
    B = "B", _("B")
    A1 = "A1", _("A1")
    C = "C", _("C")
    C1 = "C1", _("C1")
    D = "D", _("D")
    D1 = "D1", _("D1")
    E = "E", _("E")
    E1 = "E1", _("E1")
    F = "F", _("F")


class License(models.Model):
    """
    Represents a driver's license.

    Attributes:
        type (str): The type of the license (A, B, C, etc.).
        issue_date (date): The issue date of the license.
        expiry_date (date): The expiry date of the license.
        points (int): The current points of the license.

    Methods:
        is_valid(): Returns the validity of the license over time.
    """

    driver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="licenses",
        help_text=_("Driver to whom this license belongs."),
    )
    type = models.CharField(
        max_length=2,
        choices=LicenseTypes.choices,
        help_text=_("The type of the license (A, B, C, etc.)."),
    )
    issue_date = models.DateField(
        blank=False,
        validators=[
            validate_issue_date,
        ],
        help_text=_("The issue date of the license."),
    )
    expiry_date = models.DateField(
        blank=False,
        validators=[
            validate_license_validity,
        ],
        help_text=_("The expiry date of the license."),
    )
    points = models.PositiveSmallIntegerField(
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text=_("Current points of the license."),
    )
    front_image = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Upload the front image of the license."),
    )
    back_image = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        help_text=_("Upload the back image of the license."),
    )

    def __str__(self):
        return f"{self.type} - {self.expiry_date}"

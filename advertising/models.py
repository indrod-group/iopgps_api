import uuid
from django.db import models

from .utils import path_and_rename

class Advertisement(models.Model):
    """
    Model representing an advertisement.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text="UUID of the advertisement"
    )
    photo = models.ImageField(
        upload_to=path_and_rename,
        help_text="Photo for the advertisement"
    )
    url = models.URLField(
        help_text="URL linked from the advertisement"
    )
    alternate_name = models.CharField(
        max_length=255,
        help_text="Alternate name for the advertisement"
    )
    priority = models.IntegerField(
        default=0,
        help_text="Priority of the advertisement"
    )

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

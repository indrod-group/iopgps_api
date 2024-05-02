import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from mileage.models import Mileage
from movement_orders.utils import path_and_rename
from routes.models import Route
from users.models import CustomUser
from vehicles.models import Vehicle


class MovementOrder(models.Model):
    """
    Model to represent a movement order.

    A movement order is created when a vehicle is
    authorized to move from one place to another.
    The movement order records details
    about the vehicle, the driver,
    who authorized the movement, when it was created,
    the itinerary (route), the mileage at departure,
    and other details about the departure.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text=_("Unique identifier for the movement order."),
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        help_text=_("The vehicle used in the movement order."),
    )
    driver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="driven_orders",
        help_text=_("The driver of the vehicle."),
    )
    authorized_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="authorized_orders",
        help_text=_("The user who authorized the movement order."),
    )
    created_at = models.IntegerField(
        help_text=_("The creation time of the movement order in Unix time format.")
    )
    itinerary = models.ForeignKey(
        Route, on_delete=models.CASCADE, help_text=_("The route of the movement order.")
    )
    departure_mileage = models.ForeignKey(
        Mileage,
        on_delete=models.CASCADE,
        help_text=_("The mileage of the vehicle at the start of the movement order."),
    )
    departure_details = models.CharField(
        max_length=1500,
        blank=False,
        help_text=_("Details about the departure of the movement order."),
    )
    departure_time_unix = models.PositiveIntegerField(
        help_text=_("The departure time of the movement order in Unix time format.")
    )
    estimated_arrival_time_unix = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_(
            "The estimated arrival time of the movement order in Unix time format."
        ),
    )

    def __repr__(self):
        return (
            f"MovementOrder(id={self.id}, "
            f"vehicle={self.vehicle}, "
            f"driver={self.driver}, "
            f"authorized_by={self.authorized_by}, "
            f"created_at={self.created_at}, "
            f"itinerary={self.itinerary}, "
            f"departure_mileage={self.departure_mileage}, "
            f"departure_details={self.departure_details}, "
            f"departure_time_unix={self.departure_time_unix})"
        )

    def __str__(self):
        return f"id={self.id}"


class MovementOrderState(models.Model):
    """
    Model to represent a state in the lifecycle of a movement order.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text=_("Unique identifier for the movement order state."),
    )
    movement_order = models.ForeignKey(
        MovementOrder,
        on_delete=models.CASCADE,
        related_name="states",
        help_text=_("The movement order this state is associated with."),
    )
    state = models.CharField(
        max_length=200,
        help_text=_("The state of the movement order."),
    )
    timestamp_unix = models.PositiveIntegerField(
        help_text=_("The time at which this state was recorded in Unix time format.")
    )
    set_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text=_("The user who set this state."),
    )

    def __repr__(self):
        return (
            f"MovementOrderState(movement_order={self.movement_order}, "
            f"state={self.state}, "
            f"timestamp_unix={self.timestamp_unix}, "
            f"set_by={self.set_by})"
        )

    def __str__(self):
        return f"id={self.id}"


class Incident(models.Model):
    """
    Model to represent an incident that occurred during a movement order.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text=_("Unique identifier for the movement order."),
    )
    movement_order = models.ForeignKey(
        MovementOrder,
        on_delete=models.CASCADE,
        related_name="incidents",
        help_text=_("The movement order during which the incident occurred."),
    )
    description = models.CharField(
        max_length=2000,
        help_text=_("Description of the incident."),
    )
    incident_time_unix = models.IntegerField(
        help_text=_("The time of the incident in Unix time format.")
    )
    reported_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text=_("The user who reported the incident."),
    )
    resolved = models.BooleanField(
        default=False,
        help_text=_("Whether the incident has been resolved."),
    )
    image = models.ImageField(
        upload_to=path_and_rename,
        blank=True,
        null=True,
        help_text=_("Image related to the incident."),
    )

    def __repr__(self):
        return (
            f"Incident(movement_order={self.movement_order}, "
            f"description={self.description}, "
            f"incident_time_unix={self.incident_time_unix}, "
            f"reported_by={self.reported_by}, "
            f"resolved={self.resolved})"
        )

    def __str__(self):
        return f"id={self.id}"


class ClosureMovementOrder(models.Model):
    """
    Model to represent the closure of a movement order.

    The closure records details about
    the movement order being closed, who verified the closure,
    when it was confirmed, the mileage at arrival,
    the arrival time, whether the movement order was complied with,
    and any extra details about the closure.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text=_("Unique identifier for the closure of the closure movement order."),
    )
    movement_order = models.ForeignKey(
        MovementOrder,
        on_delete=models.CASCADE,
        help_text=_("The movement order being closed."),
    )
    verified_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="verified_closures",
        help_text=_("The user who verified the closure of the movement order."),
    )
    confirmation_time = models.PositiveIntegerField(
        help_text=_("The confirmation time of the closure in Unix time format.")
    )
    arrival_mileage = models.ForeignKey(
        Mileage,
        on_delete=models.CASCADE,
        help_text=_("The mileage of the vehicle at the end of the movement order."),
    )
    arrival_time_unix = models.IntegerField(
        help_text=_(
            "The arrival time of the vehicle at the destination in Unix time format."
        )
    )
    compliance = models.BooleanField(
        help_text=_("Whether the movement order was complied with.")
    )
    extra_details = models.CharField(
        max_length=1500,
        blank=True,
        help_text=_("Any extra details about the closure of the movement order."),
    )
    had_incident = models.BooleanField(
        default=False, help_text=_("Whether the movement order had any incidents.")
    )

    def __repr__(self):
        return (
            f"ClosureMovementOrder(id={self.id}, "
            f"movement_order={self.movement_order}, "
            f"verified_by={self.verified_by},"
            f"confirmation_time={self.confirmation_time}, "
            f"arrival_mileage={self.arrival_mileage}, "
            f"arrival_time_unix={self.arrival_time_unix}, "
            f"compliance={self.compliance}, "
            f"extra_details={self.extra_details})"
        )

    def __str__(self):
        return f"id={self.id}"

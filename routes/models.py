import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from alarms.models import Coordinates
from users.models import CustomUser


class Position(Coordinates):
    """
    Model to represent a geographic position.
    """

    name = models.CharField(
        max_length=200, help_text=_("Name of the position."), blank=True, null=True
    )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.lat == other.lat and self.lng == other.lng
        return False

    def __str__(self):
        return f"Position(name={self.name}, lat={self.lat}, lng={self.lng})"

    def __repr__(self):
        return self.__str__()


class Route(models.Model):
    """
    Model to represent a route, which is a collection of positions.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text=_("Unique identifier for the route."),
    )
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_routes"
    )
    name = models.CharField(max_length=200, help_text=_("Name of the route."))
    description = models.TextField(
        blank=True, help_text=_("Brief description of the route.")
    )
    positions = models.ManyToManyField(
        Position,
        through="RoutePosition",
        help_text=_("Positions that make up the route."),
        symmetrical=False,
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Route(name={self.name})"


class RoutePosition(models.Model):
    """
    Model to represent a position within a route.
    """

    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, help_text=_("The position in the route.")
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        help_text=_("The route that the position belongs to."),
    )
    order = models.PositiveIntegerField(
        help_text=_("The order of the position in the route.")
    )
    alias = models.CharField(
        max_length=200,
        help_text=_("Alias for the position."),
        blank=True,
    )

    def save(self, *args, **kwargs):
        if RoutePosition.objects.filter(
            route=self.route,
            # pylint: disable=no-member
            position__lat=self.position.lat,
            position__lng=self.position.lng,
        ).exists():
            raise ValueError(
                "A position with these coordinates already exists in this route."
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Position {self.position.name} in Route {self.route.name}"

    def __repr__(self):
        return (
            f"RoutePosition(position={self.position.name}, "
            f"route={self.route.name}, order={self.order}, "
        )


class UserRoute(models.Model):
    """
    Model representing the association between users and routes.
    A user can use multiple routes and a route can be used by multiple users.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Route"
        verbose_name_plural = "User Routes"

    def __str__(self):
        return f"User {self.user} - Route {self.route.name}"

    def __repr__(self):
        return f"UserRoute(user={self.user}, route={self.route.name})"

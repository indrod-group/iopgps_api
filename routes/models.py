from django.db import models
from django.utils.translation import gettext_lazy as _

from alarms.models import Coordinates
from users.models import CustomUser


class Position(Coordinates):
    """
    Model to represent a geographic position.
    """

    name = models.CharField(max_length=200, help_text=_("Name of the position."))

    def __str__(self):
        return f"Position(name={self.name}, lat={self.lat}, lng={self.lng})"

    def __repr__(self):
        return self.__str__()


class Route(models.Model):
    """
    Model to represent a route, which is a collection of positions.
    """

    name = models.CharField(max_length=200, help_text=_("Name of the route."))
    positions = models.ManyToManyField(
        Position,
        through="RoutePosition",
        help_text=_("Positions that make up the route."),
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
    distance = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        help_text=_("Distance to the next position in meters."),
    )
    estimated_time = models.DecimalField(
        max_digits=21,
        decimal_places=15,
        null=True,
        blank=True,
        help_text=_("Estimated time to the next position in seconds."),
    )

    def __str__(self):
        return f"Position {self.position.name} in Route {self.route.name}"

    def __repr__(self):
        return (
            f"RoutePosition(position={self.position.name}, "
            f"route={self.route.name}, order={self.order}, "
            f"distance={self.distance}, estimated_time={self.estimated_time})"
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

from django.contrib import admin
from .models import Position, Route, RoutePosition, UserRoute

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Position model.
    Displays the id, name, lat, and lng fields in the list view.
    Allows searching by name.
    """
    list_display = ['id', 'name', 'lat', 'lng']
    search_fields = ['name']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """
    Admin interface for the Route model.
    Displays the id and name fields in the list view.
    Allows searching by name.
    """
    list_display = ['id', 'creator', 'name', 'description']
    search_fields = ['name']

@admin.register(RoutePosition)
class RoutePositionAdmin(admin.ModelAdmin):
    """
    Admin interface for the RoutePosition model.
    Displays the id, position, route, order, distance, and estimated_time fields in the list view.
    Allows searching by position name and route name.
    """
    list_display = ['id', 'position', 'route', 'order', 'alias']
    search_fields = ['position__name', 'route__name']

@admin.register(UserRoute)
class UserRouteAdmin(admin.ModelAdmin):
    """
    Admin interface for the UserRoute model.
    Displays the user and route fields in the list view.
    Allows searching by user username and route name.
    """
    list_display = ['get_user', 'get_route']
    search_fields = ['user__username', 'route__name']

    def get_user(self, obj):
        return str(obj.user)
    get_user.short_description = 'User'

    def get_route(self, obj):
        return obj.route.name
    get_route.short_description = 'Route'

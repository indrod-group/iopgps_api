from django.contrib import admin
from .models import (
    Incident,
    MovementOrder,
    ClosureMovementOrder,
    MovementOrderState,
)


@admin.register(MovementOrder)
class MovementOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(MovementOrderState)
class MovementOrderStateAdmin(admin.ModelAdmin):
    pass


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    pass


@admin.register(ClosureMovementOrder)
class ClosureMovementOrderAdmin(admin.ModelAdmin):
    pass

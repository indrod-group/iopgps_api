from django.contrib import admin
from .models import MaintenanceManual, MaintenanceOperation


@admin.register(MaintenanceManual)
class MaintenanceManualAdmin(admin.ModelAdmin):
    list_display = [
        "vehicle",
        "advance_alerts",
        "minimum_frequency",
        "end_of_cycle",
    ]


@admin.register(MaintenanceOperation)
class MaintenanceOperationAdmin(admin.ModelAdmin):
    list_display = [
        "maintenance_manual",
        "system",
        "subsystem",
        "task",
        "description",
        "frequency",
    ]

from django.contrib import admin
from .models import WorkOrder, WorkOrderCompletion


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = [
        "responsible",
        "created_by",
        "vehicle",
        "issue_date_unix",
        "maintenance_type",
        "work_type",
    ]


@admin.register(WorkOrderCompletion)
class WorkOrderCompletionAdmin(admin.ModelAdmin):
    list_display = [
        "work_order",
        "status",
        "change_registered_by",
        "change_date_unix",
        "responsible_notes",
    ]

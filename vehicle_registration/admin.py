from django.contrib import admin
from .models import VehicleRegistration

@admin.register(VehicleRegistration)
class VehicleRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'issue_date', 'expiry_date']

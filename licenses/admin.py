from django.contrib import admin
from .models import License

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ['driver', 'type', 'issue_date', 'expiry_date', 'points']

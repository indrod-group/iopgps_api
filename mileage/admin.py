from django.contrib import admin
from .models import Mileage

@admin.register(Mileage)
class MileageAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'mileage', 'unit', 'unix_time_registered']

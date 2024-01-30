from django.contrib import admin
from .models import Battery, Tire, VehicleType, Vehicle, VehicleStatus, UserVehicle

@admin.register(UserVehicle)
class UserVehicleAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle',)

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(VehicleStatus)
class VehicleStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass

@admin.register(Tire)
class TireAdmin(admin.ModelAdmin):
    pass

@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    pass

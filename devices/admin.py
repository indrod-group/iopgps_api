from django.contrib import admin, messages
from .models import Device, UserDevice


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for the UserDevice model.
    Displays the users and devices fields in the list view.
    """
    list_display = ['get_user', 'get_device']

    def get_user(self, obj):
        return str(obj.user)
    get_user.short_description = 'User'

    def get_device(self, obj):
        return obj.device.imei
    get_device.short_description = 'Device'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing devices in the Django admin site.
    """

    def make_tracking_alarms(self, request, queryset):
        """
        Enable alarm tracking for the selected devices.
        """
        queryset.update(is_tracking_alarms=True)
        self.message_user(
            request,
            "El seguimiento de los dispositivos seleccionados ha sido habilitado.",
            messages.SUCCESS,
        )

    make_tracking_alarms.short_description = (
        "Habilitar seguimiento de alarmas para los dispositivos seleccionados"
    )

    def make_not_tracking_alarms(self, request, queryset):
        """
        Disable alarm tracking for the selected devices.
        """
        queryset.update(is_tracking_alarms=False)
        self.message_user(
            request,
            "El seguimiento de los dispositivos seleccionados ha sido deshabilitado.",
            messages.SUCCESS,
        )

    make_not_tracking_alarms.short_description = (
        "Deshabilitar seguimiento de alarmas para los dispositivos seleccionados"
    )


    list_display = (
        "imei",
        "user_name",
        "car_owner",
        "license_number",
        "vin",
        "is_tracking_alarms",
    )
    list_filter = (
        "is_tracking_alarms",
    )
    search_fields = ["user_name", "car_owner", "imei"]
    ordering = ["user_name"]
    actions = (
        make_tracking_alarms,
        make_not_tracking_alarms,
    )

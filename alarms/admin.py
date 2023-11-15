from django.contrib import admin
from django.utils import timezone

from .models import Alarm

@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    """
    Admin interface for the Alarm model. It allows searching by IMEI and alarm code, 
    and displays the IMEI, alarm code, and formatted alarm time in the list view. 
    The list is ordered by alarm time.
    """
    search_fields = ['device__imei', 'alarm_code']
    list_display = ['imei', 'alarm_code', 'formatted_alarm_time']
    ordering = ['time',]

    def imei(self, obj: Alarm) -> str:
        """
        Returns the IMEI of the device associated with the alarm.

        Args:
            obj (Alarm): The Alarm object.

        Returns:
            str: The IMEI of the device.
        """
        return obj.device.imei
    imei.admin_order_field = 'device__imei'  # Allows column order sorting
    imei.short_description = 'IMEI'  # Sets column header

    def formatted_alarm_time(self, obj: Alarm) -> str:
        """
        Converts the alarm time from a Unix timestamp to a formatted string.

        Args:
            obj (Alarm): The Alarm object.

        Returns:
            str: The formatted alarm time.
        """
        return timezone.datetime.fromtimestamp(obj.time).strftime('%Y-%m-%d %H:%M:%S')
    formatted_alarm_time.admin_order_field = 'time'
    formatted_alarm_time.short_description = 'Alarm Time'

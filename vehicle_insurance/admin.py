from django.contrib import admin
from .models import BrokerInfo

@admin.register(BrokerInfo)
class BrokerInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'insurance_company', 'broker_name']

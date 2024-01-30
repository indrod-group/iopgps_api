from rest_framework import serializers
from .models import License

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['driver', 'type', 'issue_date', 'expiry_date', 'points']

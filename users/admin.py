from django.contrib import admin
from rest_framework.authtoken.models import Token

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin interface for the CustomUser model.
    Displays the email, first name, last name, and role fields in the list view.
    Allows searching by email, first name, and last name.
    """
    list_display = ['email', 'first_name', 'last_name', 'role']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

    def email(self, obj):
        return obj.user.email

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # si el usuario es nuevo
            Token.objects.create(user=obj.user)

from django.contrib import admin
from .models import CustomUser, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin interface for the CustomUser model.
    Displays the email, first name, last name, roles and parent accounts in the list view.
    Allows searching by email, first name, and last name.
    """
    list_display = ['email', 'first_name', 'last_name', 'display_roles', 'display_parent_accounts']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

    def email(self, obj):
        return obj.user.email

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def display_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    display_roles.short_description = 'Roles'

    def display_parent_accounts(self, obj):
        return ", ".join([parent_account.user.username for parent_account in obj.parent_accounts.all()])
    display_parent_accounts.short_description = 'Parent Accounts'

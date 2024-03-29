from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission class that checks if the
    authenticated user is an Admin or Superuser.

    This class inherits from the BasePermission class
    provided by Django Rest Framework.
    It overrides the `has_permission` method to check
    if the authenticated user has either
    the "Admin" or "Superuser" role.
    """

    def has_permission(self, request, view):
        """
        Overridden method from BasePermission class.

        This method checks if the authenticated user
        has either the "Admin" or "Superuser" role.
        It returns True if the user has one of these roles,
        and False otherwise.

        Parameters:
        - request: The current request instance.
        - view: The view that this permission is being checked against.

        Returns:
        - bool: True if the user has the "Admin" or "Superuser" role, False otherwise.
        """
        return request.user.is_authenticated and (
            request.user.customuser.roles.filter(name="Admin").exists()
            or request.user.customuser.roles.filter(name="Superuser").exists()
        )

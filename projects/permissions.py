from rest_framework import permissions

class IsOrganizationMember(permissions.BasePermission):
    """
    Custom permission to allow only organization members to add or modify projects.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user belongs to the organization associated with the project
        return request.user.organization == obj.organization

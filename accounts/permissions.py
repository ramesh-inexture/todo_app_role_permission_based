from django.contrib.auth.models import Group
from rest_framework import permissions


# def get_group_name(user):
#     groups =  Group.objects.user_set.filter(id=user.id)
#     print("in the ",groups)
#     return groups


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups_mapping = getattr(view, "required_groups", {})

        # Determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])
        print(required_groups, "and\n", required_groups_mapping)

        # Return True if the user has all the required groups or is staff.
        return all([is_in_group(request.user, group_name) if group_name != "__all__" else True for group_name in
                    required_groups]) or (request.user and request.user.is_staff)

# from rest_framework.permissions import BasePermission
#
#
# class CustomPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated():
#             return True if request.has_perm('can_read') else False # or stuff similar to this
#         return False

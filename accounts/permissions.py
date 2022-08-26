from rest_framework.permissions import DjangoModelPermissions, BasePermission, DjangoObjectPermissions


class ModelPermission(DjangoModelPermissions):
    """ Here We have to Override DjangoModelPermissions Because It is Not Working On
    Get Method reference: https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions

    solution ref: https://stackoverflow.com/questions/67820983/djangomodelpermissions-is-not-working-for-view-level-permission-in-my-api-applic?rq=1
    """

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s', ],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsOwner(BasePermission):
    message = 'Restricted to the Owners only.'

    def has_object_permission(self, request, view, obj):
        print(obj, request.user)
        return obj == request.user


class IsOwnerOrModelPermission(ModelPermission):
    """Here we are Inheriting Custom permission named ModelPermission

    This permission returns True if user have model permission or user is owner of that object.
    To use this permission we have to go to that View then add this permission into permission_class
    and in get_object method we have to write self.check_object_permission(request, obj).

    Here def has_object_permission(self, request, view, obj) returns obj == request.user or super().has_permission(request, view)
    means user have model permission"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj == request.user or super().has_permission(request, view)

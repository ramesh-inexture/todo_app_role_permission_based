from rest_framework.permissions import DjangoModelPermissions, BasePermission


class ModelPermission(DjangoModelPermissions, BasePermission):
    """ Here We have to Override DjangoModelPermissions Because It is Not Working On
    Get Method reference: https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions"""

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s', ],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # def has_object_permission(self, request, view, obj):
    #     print(obj, request.user)
    #     return obj == request.user


class IsOwner(BasePermission):
    message = 'Restricted to the Owners only.'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        print(obj, request.user)
        return obj == request.user


# class IsOwnerOrModelModelPermission(IsOwner, ModelPermission):
#
#     def check_permissions(self):
#         if IsOwner or ModelPermission:
#             return True
#         else:
#             return False
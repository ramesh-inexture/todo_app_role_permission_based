from rest_framework.permissions import DjangoModelPermissions


class ModelPermission(DjangoModelPermissions):
    """ Here We have to Override DjangoModelPermissions Because It is Not Working On
    Get Method reference: https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions"""
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

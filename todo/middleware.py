import re

from django.http import JsonResponse


class CustomMiddleware(object):
    """To activate the middleware component, add it to the MIDDLEWARE list in Django settings
    https://stackoverflow.com/questions/18322262/how-to-set-up-custom-middleware-in-django
    ex.- MIDDLEWARE = [
        # Default Django middleware
        'django.middleware.security.SecurityMiddleware',
        ...

        # Add your custom middleware
        'path.to.your.middleware.CustomMiddleware',
        'todo.middleware.CustomMiddleware'
        ]"""
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        if request.user.is_authenticated and not request.user.is_superuser:
            email = request.user.email
            x = re.match(r'^[a-zA-Z0-9._]{3,10}\.inexture@[a-zA-Z0-9_]{1,10}\.[a-zA-Z]{2,10}$', email)
            if not x:
                return JsonResponse({'Error': 'Provided Email is not from the Organization'}, status=401)

        return response
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


# Now here we register the new ModelAdmin...
admin.site.register(User)

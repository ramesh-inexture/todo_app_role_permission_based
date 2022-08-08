from django.core.management.base import BaseCommand
from accounts.models import UserRoles


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = ['admin', 'manager', 'general']
        try:
            for roles in data:
                UserRoles.objects.create(role=roles)
                self.stdout.write("Objects Created Successfully for UserRoles")
        except Exception as e:
            self.stdout.write(f"Error: {e}")

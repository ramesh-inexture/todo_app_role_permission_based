from django.core.management.base import BaseCommand
# from accounts.models import UserRoles

""" This Command Can be Used to enter data for UserRole if we have to Create UserRoles Model
but in this Todo app we have no requirements of UserRoles model so we will not use this command
here this command is act as a reference for how to Create a Custom Command
to run this command we have to run -->  python manage.py role_input_command
"""
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         data = ['admin', 'manager', 'general']
#         try:
#             for roles in data:
#                 UserRoles.objects.create(role=roles)
#                 self.stdout.write("Objects Created Successfully for UserRoles")
#         except Exception as e:
#             self.stdout.write(f"Error: {e}")

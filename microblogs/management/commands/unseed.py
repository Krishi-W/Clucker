from django.core.management.base import BaseCommand
from microblogs.models import User

class Command(BaseCommand):
    help = "Unseeds the database, removing all users except superusers"

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        #print("WARNING: The UNSEED command has not been implemented yet.")

        users = User.objects.exclude(is_superuser=1)
        users.delete()

        print("All non-superusers successfully deleted")
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from ...models import User

class Command(BaseCommand):
    help = "Seeds the database with 100 random users"

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print("WARNING: The SEED command has not been implemented yet.")
        for x in range(100):
            username = self.faker.unique.name()
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = self.faker.unique.email()
            password = self.faker.password()
            bio = self.faker.text()

            User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                bio=bio
            ).save()

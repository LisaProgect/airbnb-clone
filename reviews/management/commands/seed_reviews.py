from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from rooms.models import Room
from users.models import User

NAME = "reviews"


class Command(BaseCommand):
    help = f"create faker {NAME} for data base"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            help=f"How menu {NAME} do you want to create",
            type=int,
            default=2,
        )

    def handle(self, *args, **options):
        number = options.get("number")
        all_users = User.objects.all()
        all_rooms = Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Review,
            number,
            {
                "accuracy": lambda x: seeder.faker.random_int(0, 5),
                "communication": lambda x: seeder.faker.random_int(0, 5),
                "cleanliness": lambda x: seeder.faker.random_int(0, 5),
                "location": lambda x: seeder.faker.random_int(0, 5),
                "check_in": lambda x: seeder.faker.random_int(0, 5),
                "value": lambda x: seeder.faker.random_int(0, 5),
                "user": lambda x: seeder.faker.random_element(all_users),
                "room": lambda x: seeder.faker.random_element(all_rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))

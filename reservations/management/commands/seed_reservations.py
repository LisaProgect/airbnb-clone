from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations.models import Reservation
from rooms.models import Room
from users.models import User

NAME = "reservations"


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
            Reservation,
            number,
            {
                "status": lambda x: seeder.faker.random_element(
                    [
                        Reservation.STATUS_CANCELED,
                        Reservation.STATUS_CONFIRMED,
                        Reservation.STATUS_PENDING,
                    ]
                ),
                "check_in": lambda x: seeder.faker.date_between("-2w", "-1d"),
                "check_out": lambda x: seeder.faker.date_between("now", "+2w"),
                "guest": lambda x: seeder.faker.random_element(all_users),
                "room": lambda x: seeder.faker.random_element(all_rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))

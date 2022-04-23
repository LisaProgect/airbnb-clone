from django.core.management.base import BaseCommand
from django_seed import Seed
from lists.models import List
from rooms.models import Room
from users.models import User

NAME = "lists"


class Command(BaseCommand):
    help = f"create faker {NAME} for data base"

    def handle(self, *args, **options):
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder = Seed.seeder()
        for user in users:
            list_model = List.objects.create(
                user=user, name=seeder.faker.sentence(nb_words=10)
            )
            to_add = rooms[
                seeder.faker.random_int(0, 5) : seeder.faker.random_int(6, 30)
            ]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{NAME} created!"))

from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):
    help = "create faker room types for data base"

    def handle(self, *args, **options):
        room_types = [
            "Single",
            "Double",
            "Triple",
            "Quad",
            "Queen",
            "King",
            "Twin",
            "Entire place",
            "Private room",
            "Shared room",
            "Hotel room",
        ]
        for room_type in room_types:

            RoomType.objects.create(name=room_type)

        self.stdout.write(self.style.SUCCESS("Successfully created room types"))

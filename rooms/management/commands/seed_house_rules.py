from django.core.management.base import BaseCommand
from rooms.models import HouseRule

NAME = "house rules"


class Command(BaseCommand):
    help = f"create faker {NAME} for data base"

    def handle(self, *args, **options):
        house_rules = [
            "Not suitable for infants (under 2 years)",
            "No smoking",
            "No pets",
            "No parties or events",
            "Pets are allowed",
            "Smoking is allowed",
        ]
        for rule in house_rules:

            HouseRule.objects.create(name=rule)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {NAME}"))

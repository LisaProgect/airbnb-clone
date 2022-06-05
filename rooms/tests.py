import logging
import datetime
from unittest.mock import patch
from django_seed import Seed
from django.test import TestCase

from .models import Room
from users.models import User
from cal import Calendar, Day

seeder = Seed.seeder()


class RoomModelTestCase(TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.number_of_rooms = 3
        user = User.objects.create_user("SomeName", password="123df")
        seeder.add_entity(
            Room,
            self.number_of_rooms,
            {
                "host": lambda x: user,
            },
        )
        seeder.execute()
        self.qs = Room.objects.all()

    def test_queryset_exists(self):
        self.assertTrue(self.qs.exists())

    def test_queryset_count(self):
        self.assertEqual(self.qs.count(), self.number_of_rooms)

    def test_method_get_calendars_return_cal(self):
        room = self.qs[0]
        cal1, cal2 = room.get_calendars()
        self.assertTrue(isinstance(cal1, Calendar))
        self.assertTrue(isinstance(cal2, Calendar))

    def test_method_get_calendars_return_current_month(self):
        room = self.qs[0]
        cal1, _ = room.get_calendars()
        self.assertEqual(cal1.month, datetime.datetime.now().month)

    @patch("django.utils.timezone.now", lambda: datetime.datetime(2022, 12, 29))
    def test_method_get_calendars_return_next_month(self):
        room = self.qs[0]
        _, cal2 = room.get_calendars()
        self.assertEqual(cal2.month, 1)


class CalendarTestCase(TestCase):
    def setUp(self):
        self.cal = Calendar(2022, 6)

    def test_days(self):
        days_another_month = 5
        days_in_month = 30
        list_days = self.cal.get_days()
        day = list_days[0]
        self.assertEqual(len(list_days), days_another_month + days_in_month)
        self.assertTrue(isinstance(list_days[0], Day))
        self.assertTrue("number" in dir(day))

    def test_month(self):
        name_month = "June"
        self.assertEqual(self.cal.get_month(), name_month)
        self.assertNotEqual(self.cal.get_month(), "September")

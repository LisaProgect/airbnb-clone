from django.contrib import admin
from .models import BookedDay, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin Definition"""

    list_display = (
        "room",
        "guest",
        "status",
        "check_in",
        "check_out",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)


@admin.register(BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    """Booked Day Admin Definition"""

    list_display = (
        "day",
        "reservation",
        "reservation_guest",
    )

    @admin.display(description="Host", ordering="reservation__guest")
    def reservation_guest(self, obj):
        return obj.reservation.guest

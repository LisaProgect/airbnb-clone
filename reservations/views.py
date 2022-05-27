from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View
from reservations.models import BookedDay, Reservation
from reviews.forms import CreateReviewForm
from rooms.models import Room


class CreateError(Exception):
    pass


@login_required(login_url="/users/login/")
def create(request, room_pk, year, month, day):
    try:
        room = Room.objects.get(pk=room_pk)
        date_obj = timezone.datetime(year, month, day)
        BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (Room.DoesNotExist, CreateError):
        messages.error(request, "You can't reserve this room")
        return redirect(reverse("core:home"))
    except BookedDay.DoesNotExist:
        reservation = Reservation.objects.create(
            check_in=date_obj,
            check_out=date_obj + timezone.timedelta(days=1),
            guest=request.user,
            room=room,
        )
        print(reservation)
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = Reservation.STATUS_CONFIRMED
    if verb == "cancel":
        reservation.status = Reservation.STATUS_CANCELED
        BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Update")
    return redirect(reverse("reservations:detail", kwargs={"pk": pk}))

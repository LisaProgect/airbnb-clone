from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reviews.forms import CreateReviewForm
from rooms.models import Room


@login_required(login_url="/users/login/")
def create_review(request, room_pk):
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        room = Room.objects.get_or_none(pk=room_pk)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            form.save(room, request.user)
            messages.success(request, "Room reviewed")
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))

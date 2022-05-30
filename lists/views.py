from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rooms.models import Room
from lists.models import List


@login_required(login_url="/users/login/")
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, created = List.objects.get_or_create(
            user=request.user, name="My favorite Houses"
        )
        if action == "remove":
            the_list.rooms.remove(room)
        else:
            the_list.rooms.add(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):
    template_name = "lists/list_detail.html"

from django.shortcuts import render
from django.views.generic import DetailView
from rooms.models import Room

# Create your views here.


class RoomDetail(DetailView):
    """RoomDetail Definition"""

    model = Room

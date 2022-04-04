from django.contrib import admin
from .models import Room, RoomType, Facility, HouseRule, Amenity, Photo


@admin.register(RoomType, Facility, HouseRule, Amenity)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

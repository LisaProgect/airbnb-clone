from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Room, RoomType, Facility, HouseRule, Amenity, Photo


@admin.register(RoomType, Facility, HouseRule, Amenity)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = (
        "name",
        "use_by",
    )

    def use_by(self, obj):
        return obj.rooms.count()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    @admin.display(description="Thumbnail")
    def get_thumbnail(self, obj):
        return mark_safe(f'<img src={obj.file.url} width="50px"/>')


class PhotoInline(admin.TabularInline):
    """Photo Inline Definition"""

    model = Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "classes": ("collapse",),
                "fields": ("name", "description", "country", "city", "address"),
            },
        ),
        (
            "Times",
            {
                "classes": ("collapse",),
                "fields": ("check_in", "check_out"),
            },
        ),
        (
            "More about space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Spaces",
            {
                "classes": ("collapse",),
                "fields": ("room_types", "beds", "bedrooms", "bath", "guests"),
            },
        ),
        (
            "Last details",
            {
                "classes": ("collapse",),
                "fields": ("instant_book", "price", "host"),
            },
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "bath",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_types",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "host__superhost",
        "amenities",
        "facilities",
        "house_rules",
        "instant_book",
        "city",
        "country",
    )

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    search_fields = ("city", "country", "^host__username")

    def count_photos(self, obj):
        return obj.photos.count()

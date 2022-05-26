from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, View, UpdateView, FormView
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from rooms.models import Room, Photo
from rooms.forms import SearchForm, CreatePhotoForm, CreateRoomForm
from users import mixins as user_mixins


class RoomDetail(DetailView):
    """RoomDetail Definition"""

    model = Room


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = instant_book

                if superhost is True:
                    filter_args["host__superhost"] = superhost

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},
                )
        else:
            form = SearchForm()

        return render(
            request,
            "rooms/search.html",
            {"form": form},
        )


class EditRoomView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    """RoomDetail Definition"""

    model = Room
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )
    template_name = "rooms/room_edit.html"
    success_message = "Room updated"

    def get_object(self, queryset=None):
        room = super().get_object(queryset)
        user_pk = self.request.user.pk
        host_pk = room.host.pk
        if host_pk == user_pk:
            return room
        raise Http404()


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset)
        user_pk = self.request.user.pk
        host_pk = room.host.pk
        if host_pk == user_pk:
            return room
        raise Http404()


@login_required(login_url="/users/login/")
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        photo = Photo.objects.filter(room__pk=room_pk, pk=photo_pk).first()
        host = photo.room.host
        if host.pk != user.pk:
            messages.error(request=request, message="You can't delete this photo")
            return redirect(reverse("core:home"))
        else:
            photo.delete()
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except Photo.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = Photo
    template_name = "rooms/photo_edit.html"
    fields = ("caption",)
    pk_url_kwarg = "photo_pk"
    success_message = "Photo updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})

    def get_object(self, queryset=None):
        photo = super().get_object(queryset)
        user_pk = self.request.user.pk
        host_pk = photo.room.host.pk
        if host_pk == user_pk:
            return photo
        raise Http404()


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    template_name = "rooms/photo_create.html"
    form_class = CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk=pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):
    template_name = "rooms/room_create.html"
    form_class = CreateRoomForm

    def form_valid(self, form):
        room = form.save(self.request.user)
        messages.success(self.request, "Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

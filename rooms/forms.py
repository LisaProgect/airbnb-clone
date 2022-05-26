from django import forms
from django_countries.fields import CountryField
from rooms.models import Facility, RoomType, Amenity, Photo, Room


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="UA").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=RoomType.objects.all()
    )
    price = forms.IntegerField(required=False, min_value=0)
    guests = forms.IntegerField(required=False, min_value=0, max_value=10)
    beds = forms.IntegerField(required=False, min_value=0, max_value=10)
    bedrooms = forms.IntegerField(required=False, min_value=0, max_value=10)
    baths = forms.IntegerField(required=False, min_value=0, max_value=10)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = (
            "caption",
            "file",
        )

    def save(self, pk, commit=True):
        photo = super().save(commit=False)
        room = Room.objects.get(pk=pk)
        photo.room = room
        if commit:
            photo.save()
        return photo


class CreateRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["check_in"].widget.attrs["placeholder"] = "00:00:00"
        self.fields["check_out"].widget.attrs["placeholder"] = "00:00:00"

    class Meta:
        model = Room
        exclude = ["host"]

    def save(self, user, commit=True):
        room = super().save(commit=False)
        room.host = user
        if commit:
            room.save()
            self.save_m2m()
        return room

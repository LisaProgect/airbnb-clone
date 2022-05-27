from django.urls import path
from reservations.views import ReservationDetailView, create, edit_reservation

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room_pk>/<int:year>-<int:month>-<int:day>", create, name="create"
    ),
    path("<int:pk>", ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>", edit_reservation, name="edit"),
]

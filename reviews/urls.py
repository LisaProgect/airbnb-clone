from django.urls import path
from reviews.views import create_review

app_name = "reviews"

urlpatterns = [
    path("create/<int:room_pk>/", create_review, name="create"),
]

from django.urls import path
from users.views import LoginView, logout_user

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_user, name="logout"),
]

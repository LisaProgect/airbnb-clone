from django.urls import path
from users.views import LoginView, SingUpView, logout_user, complete_verification

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_user, name="logout"),
    path("signup", SingUpView.as_view(), name="signup"),
    path("verify/<str:key>/", complete_verification, name="complete-verification"),
]

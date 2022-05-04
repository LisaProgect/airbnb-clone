from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, SingUpForm
from users.models import User


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy("core:home")
    template_name = "users/login.html"

    def form_valid(self, form):

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=email, password=password)

        if user is not None:
            login(request=self.request, user=user)
        return super().form_valid(form)


def logout_user(request):
    logout(request=request)
    return redirect(reverse("core:home"))


class SingUpView(FormView):
    template_name = "users/signup.html"
    form_class = SingUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Lisa",
        "last_name": "LastName",
        "email": "lisalis@vivaldi.net",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=email, password=password)

        if user is not None:
            login(request=self.request, user=user)
        user.verify_email(uri=self.request.build_absolute_uri("/"))
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key, email_verified=False)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))

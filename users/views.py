from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm


class LoginView(FormView):
    form_class = LoginForm
    http_method_names = ["get", "post"]
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

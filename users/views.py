import os
import requests
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from users.forms import LoginForm, SingUpForm
from users.models import User
from users.mixins import LoggedInOnlyView, LoggedOutOnlyView, EmailLoginOnlyView


class LoginView(LoggedOutOnlyView, FormView):
    form_class = LoginForm
    template_name = "users/login.html"

    def form_valid(self, form):

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=email, password=password)

        if user is not None:
            login(request=self.request, user=user)
            messages.success(
                request=self.request, message=f"Welcome back {user.first_name}"
            )
        else:
            messages.error(
                request=self.request, message="Somthing was wrong, try log in again"
            )
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def logout_user(request):
    logout(request=request)
    return redirect(reverse("core:home"))


class SingUpView(FormView):
    template_name = "users/signup.html"
    form_class = SingUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(request=self.request, username=email, password=password)

        if user is not None:
            login(request=self.request, user=user)
            user.verify_email(uri=self.request.build_absolute_uri("/"))
            messages.success(
                request=self.request,
                message="You are success Sing up. Please verify your email",
            )
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key, email_verified=False)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        messages.success(
            request=request, message="You are success complete verification"
        )
    except User.DoesNotExist:
        messages.error(request=request, message="User does not exist")
    return redirect(reverse("core:home"))


def github_login(request):
    redirect_uri = request.build_absolute_uri(reverse("users:github-callback"))
    client_id = os.environ.get("GH_ClIENT_ID")
    query_string = urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "user",
        },
        safe=":/,",
    )
    return redirect(f"https://github.com/login/oauth/authorize?{query_string}")


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is not None:
            client_id = os.environ.get("GH_ClIENT_ID")
            client_secret = os.environ.get("GH_CLIENT_SECRETS")
            url_github_token = "https://github.com/login/oauth/access_token"
            data_token = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
            }
            token_request = requests.post(
                url_github_token,
                data=data_token,
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                url_github_profile = "https://api.github.com/user"
                header = {
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json",
                }
                profile_request = requests.get(url_github_profile, headers=header)
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                email = profile_json.get("email")
                if email is None:
                    url_github_emails = "https://api.github.com/user/emails"
                    emails_request = requests.get(url_github_emails, headers=header)
                    emails_json = emails_request.json()
                    (email_info,) = list(
                        filter(
                            lambda email: email["verified"]
                            and email["visibility"] == "private",
                            emails_json,
                        )
                    )
                    email = email_info["email"]
                if username is not None:
                    name = profile_json.get("name") or username
                    bio = profile_json.get("bio") or ""
                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except User.DoesNotExist:
                        user = User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request=request, message=e)
        return redirect(reverse("core:home"))


class ProfileDetailView(DetailView):
    model = User
    context_object_name = "user_obj"


class ProfileUpdateView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "users/update_profile.html"
    fields = [
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthday",
        "language",
        "currency",
    ]

    success_message = "Update successful"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for _, field in form.fields.items():
            field.widget.attrs["placeholder"] = field.label
        return form


class UpdatePasswordView(
    LoggedInOnlyView, EmailLoginOnlyView, SuccessMessageMixin, PasswordChangeView
):
    template_name = "users/update-password.html"
    success_message = "Update successful"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for _, field in form.fields.items():
            field.widget.attrs["placeholder"] = field.label
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required(login_url="/users/login/")
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(request.META.get("HTTP_REFERER"))

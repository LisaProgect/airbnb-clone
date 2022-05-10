import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):
    """
    Custom User Model
    """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_UKRAINIAN = "uk"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_UKRAINIAN, "Ukrainian"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_UAH = "uah"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_UAH, "UAH"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=10)
    bio = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, blank=True, max_length=2, default=LANGUAGE_ENGLISH
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, blank=True, max_length=3, default=CURRENCY_USD
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        choices=LOGIN_CHOICES, blank=True, max_length=20, default=LOGIN_EMAIL
    )

    def verify_email(self, uri):
        """If the email isn't verify, send mail with secret cod for verification."""
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                template_name="emails/verify_email.html",
                context={"uri": uri, "secret": secret},
            )
            print(uri, html_message)
            send_mail(
                subject="Verify Airbnb Account",
                message=strip_tags(html_message),
                from_email=f"{settings.EMAIL_HOST_USER}",
                recipient_list=[self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

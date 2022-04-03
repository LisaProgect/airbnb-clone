from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin
    """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "bio",
                    "gender",
                    "avatar",
                    "birthday",
                    "language",
                    "currency",
                    "superhost",
                ),
            },
        ),
    )

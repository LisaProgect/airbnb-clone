from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    "password", forms.ValidationError(message="Password is wrong")
                )
        except User.DoesNotExist:
            self.add_error(
                "email", forms.ValidationError(message="User does not exist")
            )


class SingUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs["placeholder"] = field.label

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")
        exclude = ("username",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        user.username = email
        if commit:
            user.save()
        return user

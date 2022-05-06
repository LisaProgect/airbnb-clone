from django import forms
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

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

    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

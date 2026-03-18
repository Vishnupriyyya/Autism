"""Authentication and registration forms."""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Registration form for new users (Parents)."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.PARENT
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Login form with Bootstrap-friendly styling."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )

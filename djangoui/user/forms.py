"""Overide default django forms."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    """Update user Creation form."""

    email = forms.EmailField()

    class Meta:
        """Spec model and fields."""

        model = User
        fields = ['username', 'email', 'password1', 'password2']

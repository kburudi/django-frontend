"""Overide default django forms."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    """Update user Creation form."""

    email = forms.EmailField()

    class Meta:
        """Spec model and fields."""

        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Update username, email and password form."""

    email = forms.EmailField()

    class Meta:
        """Fields we will be updating."""

        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Update user profile data form."""

    class Meta:
        """Fields we will be updating."""

        model = Profile
        fields = ['image', 'first_name', 'other_names', 'phone_number', 'bio']

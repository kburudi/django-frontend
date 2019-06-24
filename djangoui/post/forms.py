"""Overide default django forms."""

from django import forms
from .models import Post


class CreateUpdatePostForm(forms.ModelForm):
    """Create and Update user profile data form."""

    class Meta:
        """Fields we will be updating."""

        model = Post
        fields = ['image', 'title', 'description']

"""Users CRUD and etc."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.urls import reverse
from djangoui.post.models import Post
from .models import Profile
from .forms import (
    UserRegistrationForm, UserUpdateForm,
    ProfileUpdateForm
)


@login_required
def logout(request):
    """Logout the user."""
    user = request.user
    django_logout(request)

    return redirect('login')


def register(request):
    """Create new user form."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! \n'  # noqa
                             'Please login!!!')

            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Show user profile."""
    posts = Post.objects.filter(author=request.user)

    if request.POST:
        profile = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        up_form = UserUpdateForm(request.POST, instance=request.user)

        if profile.is_valid() and up_form.is_valid():
            up_form.save()
            profile.save()

        messages.success(request, 'Your account details have been updated')
        return redirect('profile')

    else:
        profile = ProfileUpdateForm(instance=request.user.profile)
        up_form = UserUpdateForm(instance=request.user)

    context = {
        'profile': profile,
        'posts': posts,
        'up_form': up_form,
    }
    return render(request, 'users/profile.html', context)

"""Users CRUD and etc."""

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.urls import reverse


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
            messages.success(request, f'Account created for {username}! \n'
                             'Please login!!!')

            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

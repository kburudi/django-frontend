"""View for posts."""

from django.shortcuts import render
from .models import Post


def show_posts(request):
    """Show posts view."""
    posts = Post.objects.all()

    return render(request, 'posts/home.html', {'posts': posts})


def about_page(request):
    """About page."""
    return render(request, 'posts/about.html', {'title': 'about'})

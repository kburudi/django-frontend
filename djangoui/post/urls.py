"""Urls for posts."""
from django.urls import path, include
from .views import show_posts, about_page

blog_url_patterns = [
]

urlpatterns = [
    path('', show_posts, name='ui-posts'),
    path('about/', about_page, name='ui-about'),
]

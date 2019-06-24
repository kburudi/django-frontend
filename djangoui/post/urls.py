"""Urls for posts."""
from django.urls import path, include
from .views import (
    about_page,
    PostListView,
    SinglePostView,
    CreatePostView,
    UpdatePostView,
    DeletePostView
)

blog_url_patterns = [
    path('<int:pk>/', SinglePostView.as_view(), name='single-post'),
    path('new/', CreatePostView.as_view(), name='new-post'),
    path('<int:pk>/update/', UpdatePostView.as_view(), name='update-post'),
    path('<int:pk>/delete/', DeletePostView.as_view(), name='delete-post'),
]

urlpatterns = [
    path('', PostListView.as_view(),
         name='ui-posts'),
    path('about/', about_page, name='ui-about'),
    path('posts/', include(blog_url_patterns)),
]

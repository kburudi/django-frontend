"""View for posts."""

from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import CreateUpdatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
import itertools


def show_posts(request):
    """Show posts view."""
    posts = Post.objects.all()

    return render(request, 'post/home.html', {'posts': posts})


def gen_slug(user, title):
        """Generate slug for a post."""
        new_slug = orig = slugify(
            "{0} {1}".format(str(user), title))

        for x in itertools.count(1):
            if not Post.objects.filter(slug=new_slug).exists():
                break
            new_slug = '%s-%d' % (orig, x)

        return new_slug


class PostListView(ListView):
    """List all posts."""

    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class SinglePostView(DetailView):
    """Retrieve single post."""

    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    """Retrieve single post."""

    model = Post
    form_class = CreateUpdatePostForm

    def form_valid(self, form):
        """Alter post method."""
        print(form.instance.image)
        form.instance.author = self.request.user
        form.instance.slug = gen_slug(self.request.user, form.instance.title)
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Retrieve single post."""

    model = Post
    form_class = CreateUpdatePostForm

    def test_func(self):
        """Ensure only owner can edit post."""
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Retrieve single post."""

    model = Post
    success_url = "/"

    def form_valid(self, form):
        """Alter post method."""
        print(form.instance.image)
        form.instance.author = self.request.user
        form.instance.slug = gen_slug(self.request.user, form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        """Ensure only owner can edit post."""
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about_page(request):
    """About page."""
    return render(request, 'post/about.html', {'title': 'about'})

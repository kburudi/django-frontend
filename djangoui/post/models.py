"""Model for posts."""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import itertools


class Post(models.Model):
    """Fields and props for posts model."""

    title = models.CharField(max_length=259)
    slug = models.SlugField(max_length=200, unique=True, default='some-post')
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Display posts title."""
        return self.title

    def display_text(self):
        """Limit printedt text."""
        dots = "..."
        mini_desc = self.description[0:98]
        return "{0}{1}".format(mini_desc, dots)

    def display_title(self):
        """Limit Display title."""
        if len(self.title) > 55:
            return self.title[0:56]
        return self.title

    def gen_slug(self):
        """Generate slug for a post."""
        new_slug = orig = slugify(
            "{0} {1}".format(str(self.author), self.title))

        for x in itertools.count(1):
            if not self.objects.filter(slug=new_slug).exists():
                break
            new_slug = '%s-%d' % (orig, x)

        return new_slug

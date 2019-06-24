"""Model for posts."""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse
# from django.contrib import messages


def create_image_path(instance, filename):
    """Change path to files and image name."""
    print('\n\n', filename, '\n\n')
    ext = filename.split('.')[-1]
    time_saved = str(timezone.now()).split(' ')
    min_hour_sec = '-'.join(time_saved[1].split('.')[0].split(':'))
    time_saved[1] = min_hour_sec
    time_saved = '-'.join(time_saved)
    filename = time_saved + "-post-" + instance.author.username + '.' + ext

    return '/'.join(['posts_pics', instance.author.username, filename])


class Post(models.Model):
    """Fields and props for posts model."""

    title = models.CharField(max_length=259)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(default='post.jpg',
                              upload_to=create_image_path)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Display posts title."""
        return self.title

    def display_text(self):
        """Limit printedt text."""
        dots = "..."
        mini_desc = self.description[0:90]
        return "{0}{1}".format(mini_desc, dots)

    def display_title(self):
        """Limit Display title."""
        if len(self.title) > 55:
            return self.title[0:56]
        return self.title

    def get_absolute_url(self):
        """Redirect after create post."""
        return reverse('single-post', kwargs={'pk': self.pk})

    def set_author(self, request):
        """Create Post author."""
        self.author = request.user

    def save(self, *args, **kwargs):
        """Overide save image."""
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
            img.thumbnail(output_size)
            img.save(self.image.path)

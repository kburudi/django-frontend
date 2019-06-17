"""Model for posts."""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
import itertools


class Post(models.Model):
    """Fields and props for posts model."""

    title = models.CharField(max_length=259)
    slug = models.SlugField(max_length=200, unique=True, default='some-post')
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(default='post.jpg', upload_to="posts_pics")
    # img_thumb = models.ImageField(default='post.jpg', upload_to="posts_thumbs") # noqa
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

    def gen_slug(self):
        """Generate slug for a post."""
        new_slug = orig = slugify(
            "{0} {1}".format(str(self.author), self.title))

        for x in itertools.count(1):
            if not self.objects.filter(slug=new_slug).exists():
                break
            new_slug = '%s-%d' % (orig, x)

        return new_slug

    def save(self):
        """Overide save image."""
        super().save()

        img = Image.open(self.image.path)

        # renaming images
        img_new_name = self.rename_image()

        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
            img.thumbnail(output_size)
            img.save(img_new_name)
        else:
            img.save(img_new_name)

    def rename_image(self):
        """Rename images."""
        new_image_path_name = self.image.path.split('/')
        ext = new_image_path_name[-1].split('.')[-1]
        imgname = new_image_path_name[-1].split('.')[0]
        time_saved = str(timezone.now()).split(' ')
        min_hour_sec = '-'.join(time_saved[1].split('.')[0].split(':'))
        time_saved[1] = min_hour_sec
        time_saved = '-'.join(time_saved)
        new_name = f'{self.author.username}-{time_saved}-post-{self.id}-image.{ext}'  # noqa
        new_image_path_name[-1] = new_name
        new_image_path_name = '/'.join(new_image_path_name)
        return new_image_path_name

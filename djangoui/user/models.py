"""Model for user accounts."""

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


def creaet_image_path(instance, filename):
    """Change path to prof image  and save new name."""
    ext = filename.split('.')[-1]
    time_saved = str(timezone.now()).split(' ')
    min_hour_sec = '-'.join(time_saved[1].split('.')[0].split(':'))
    time_saved[1] = min_hour_sec
    time_saved = '-'.join(time_saved)
    filename = time_saved + "-pic-" + instance.user.username + '.' + ext

    return '/'.join(['profiles', instance.user.username, filename])


class Profile(models.Model):
    """User profile creation model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,
                                  blank=True, null=True)
    other_names = models.CharField(max_length=62,
                                   blank=True, null=True)
    bio = models.TextField(max_length=700,
                           blank=True, null=True)
    other_email = models.EmailField(max_length=200, unique=True,
                                    blank=True, null=True)
    phone_number = models.CharField(max_length=50,
                                    blank=True, null=True)
    GUID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(default='default.jpg',
                              upload_to=creaet_image_path)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Name to be shown instead of object."""
        return "{0} {1}".format(self.other_names, self.first_name)

    def save(self, *args, **kwargs):
        """Overide save profile."""
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

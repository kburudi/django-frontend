"""Model for user accounts."""

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class Profile(models.Model):
    """User profile creation model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,
                                  blank=True, null=True)
    other_names = models.CharField(max_length=62,
                                   blank=True, null=True)
    image = models.CharField(max_length=250,
                             blank=True, null=True)
    bio = models.TextField(max_length=700,
                           blank=True, null=True)
    other_email = models.EmailField(max_length=200, unique=True,
                                    blank=True, null=True)
    phone_number = models.CharField(max_length=50,
                                    blank=True, null=True)
    GUID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(default='default.jpg', upload_to="profile_pic")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Name to be shown instead of object."""
        return "{0} {1}".format(self.other_names, self.first_name)

    def save(self):
        """Overide save profile."""
        super().save()

        img = Image.open(self.image.path) # noqa
        new_image_path_name = self.image.path.split('/')
        ext = new_image_path_name[-1].split('.')[-1]
        imgname = new_image_path_name[-1].split('.')[0]
        time_saved = str(timezone.now()).split(' ')
        min_hour_sec = '-'.join(time_saved[1].split('.')[0].split(':'))
        time_saved[1] = min_hour_sec
        time_saved = '-'.join(time_saved)
        new_name = f'{self.user.username}-{time_saved}-profile.{ext}' # noqa
        new_image_path_name[-1] = new_name
        new_image_path_name = '/'.join(new_image_path_name)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(new_image_path_name)

import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username
    
class UserFollowing(models.Model):
    follower_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower_user.username} follows {self.following_user.username}'


class UserProfileInfo(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # additional attributes for user
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_pic:
            # resize the image
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                # create a thumbnail
                img = img.resize(output_size, Image.Resampling.LANCZOS)
                # overwrite the larger image
                img.save(self.profile_pic.path)

    def delete(self, *args, **kwargs):
        if self.profile_pic:
            os.remove(self.profile_pic.path)
        super(UserProfileInfo, self).delete(*args, **kwargs)

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
    ws_state = models.BooleanField(default=False)
    channel_name = models.CharField(max_length=255, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username


class UserFollowing(models.Model):
    follower_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower_user.username} follows {self.following_user.username}'


class ProfileBanner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class BannerChoices(models.TextChoices):
        BANNER_1 = settings.BANNER_1_URL
        BANNER_2 = settings.BANNER_2_URL
        BANNER_3 = settings.BANNER_3_URL
        BANNER_4 = settings.BANNER_4_URL

    profile_banner = models.CharField(max_length=255,
                                      choices=BannerChoices.choices,
                                      default=BannerChoices.BANNER_1)

    def __str__(self):
        return f'{self.user.username} Banner'

    def get_banner_choices(self):
        # return self.BannerChoices.names
        return self.BannerChoices.choices
    
    def get_test(self):
        return self.BannerChoices.choices
        # return getattr(self.BannerChoices, "BANNER_1", None)
    
    def get_profile_banner(self):
        # return self.profile_banner.url if self.profile_banner else settings.DEFAULT_BANNER_URL
        return self.profile_banner


class UserProfileInfo(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # additional attributes for user
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_profile_pic(self):
        return self.profile_pic.url if self.profile_pic else settings.DEFAULT_IMAGE_URL

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_pic and self.profile_pic.path != settings.DEFAULT_IMAGE_URL:
            # resize the image
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                # create a thumbnail
                img = img.resize(output_size, Image.Resampling.LANCZOS)
                # overwrite the larger image
                img.save(self.profile_pic.path)


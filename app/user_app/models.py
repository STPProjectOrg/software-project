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
    follower_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower_user.username} follows {self.following_user.username}'


class UserProfileInfo(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # additional attributes for user
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)
    profile_banner = models.ImageField(
        upload_to='banner_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_profile_pic(self):
        return self.profile_pic.url if self.profile_pic else settings.DEFAULT_IMAGE_URL

    def get_profile_banner(self):
        return self.profile_banner.url if self.profile_banner else settings.DEFAULT_BANNER_URL 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        is_profile_pic_changed = self.has_changed('profile_pic')
        is_profile_banner_changed = self.has_changed('profile_banner')

        if is_profile_pic_changed:
            if self.profile_pic and self.profile_pic.path != settings.DEFAULT_IMAGE_URL:
                # resize the image
                img = Image.open(self.profile_pic.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    # create a thumbnail
                    img = img.resize(output_size, Image.Resampling.LANCZOS)
                    # overwrite the larger image
                    img.save(self.profile_pic.path)

        if is_profile_banner_changed:
            if self.profile_banner and self.profile_banner.path != settings.DEFAULT_BANNER_URL:
                img = Image.open(self.profile_banner.path)
                if img.height > 800 or img.width > 1200:
                    output_size = (1200, 800)
                    img = img.resize(output_size, Image.LANCZOS)
                    img.save(self.profile_banner.path)

    def has_changed(self, field_name):
        if self.pk is None:
            return True

        old_value = self.__class__._default_manager.filter(
            pk=self.pk).values(field_name).get()[field_name]
        new_value = getattr(self, field_name)
        return old_value != new_value

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     if self.profile_pic and self.profile_pic.path != settings.DEFAULT_IMAGE_URL:
    #         # resize the image
    #         img = Image.open(self.profile_pic.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             # create a thumbnail
    #             img = img.resize(output_size, Image.Resampling.LANCZOS)
    #             # overwrite the larger image
    #             img.save(self.profile_pic.path)

    # OLD #
    '''
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
    '''

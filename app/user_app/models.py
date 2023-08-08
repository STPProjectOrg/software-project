from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from PIL import Image


class CustomUser(AbstractUser):
    """
    Custom user model extending the AbstractUser class.
    """
    
    # User fields
    username = models.CharField(max_length=30, blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)
    biography = models.TextField(blank=True) # Optional biography field
    ws_state = models.BooleanField(default=False) # Custom field indicating work state

    # Required fields for user creation
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        """
        Return the string representation of the user.
        """
        return self.username


class UserFollowing(models.Model):
    """
    Model representing the relationship between users who follow and are followed.
    """
    
    # ForeignKey to represent the follower user
    follower_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    
    # ForeignKey to represent the following user
    following_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followers')
    
    # Timestamp for when the relationship was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the relationship.
        """
        return f'{self.follower_user.username} follows {self.following_user.username}'


class ProfileBanner(models.Model):
    """
    Model representing the profile banner for a user.
    """

    # OneToOneField to link the profile banner to a user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class BannerChoices(models.TextChoices):
        """
        Enumerated choices for the profile banner.
        """
        BANNER_1 = settings.BANNER_1_URL
        BANNER_2 = settings.BANNER_2_URL
        BANNER_3 = settings.BANNER_3_URL
        BANNER_4 = settings.BANNER_4_URL

    # CharField to store the chosen profile banner with choices
    profile_banner = models.CharField(max_length=255,
                                      choices=BannerChoices.choices,
                                      default=BannerChoices.BANNER_1)
    
    def __str__(self):
        """
        Return a string representation of the profile banner.
        """
        return f'{self.user.username} Banner'
    
    def get_banner_choices(self):
        """
        Get the available choices for the profile banner.
        """
        return self.BannerChoices.choices
    
    def get_profile_banner(self):
        """
        Get the URL of the user's profile banner.
        """
        return self.profile_banner


class UserProfileInfo(models.Model):
    """
    Model representing users profile picture.
    """

    # OneToOneField to link the user profile info to a user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # ImageField to store the user's profile picture
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)
    
    def __str__(self):
        """
        Return a string representation of the user's profile.
        """
        return f'{self.user.username} Profile'
    
    def get_profile_pic(self):
        """
        Get the URL of the user's profile picture, or use the default image.
        """
        return self.profile_pic.url if self.profile_pic else settings.DEFAULT_IMAGE_URL

    def save(self, *args, **kwargs):
        """
        Override the save method to resize and save the profile picture.
        """
        super().save(*args, **kwargs)

        if self.profile_pic and self.profile_pic.path != settings.DEFAULT_IMAGE_URL:
            # Resize the image if it's larger than 300x300
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img = img.resize(output_size, Image.Resampling.LANCZOS)
                img.save(self.profile_pic.path)

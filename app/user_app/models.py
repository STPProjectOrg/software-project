from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username


class UserProfileInfo(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # additional attributes for user 
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
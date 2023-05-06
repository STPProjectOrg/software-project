from django.db import models

from user_app.models import CustomUser


# Create your models here.


class Settings(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    settings = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.settings

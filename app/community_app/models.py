from django.db import models
from user_app.models import CustomUser
from api_app.models import Asset
# Create your models here.


class Post(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    tags = models.CharField(max_length=100)
    # privacySettings = models.CharField()

    def __str__(self):
        return self.user_id


class Like(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Comment(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateField()

    def __str__(self):
        return self.user_id

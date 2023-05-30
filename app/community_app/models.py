from django.db import models
from user_app.models import CustomUser
from api_app.models import Asset
# Create your models here.

class Posts(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    hashtags = models.CharField(max_length=100)
    #privacySettings = models.CharField()
    
    def __str__(self):
        return self.user_id

class PostLikes(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id

class PostComments(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user_id
    
class CommentLikes(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(PostComments, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id

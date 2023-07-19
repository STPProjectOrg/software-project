from django.db import models
from user_app.models import CustomUser
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    tags = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images/', blank=True)
    privacy_settings = models.CharField(max_length=10, default="all")

    def __str__(self):
        return self.content


class PostLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    image = models.ImageField(upload_to='comment_images/', blank=True)

    def __str__(self):
        return self.user
    
class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id
    
class Tag(models.Model):
    tagname = models.CharField(max_length=20)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

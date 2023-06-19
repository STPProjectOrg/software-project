from django.test import SimpleTestCase
from django.urls import reverse, resolve
from community_app.views import main, comment, post
from community_app.models import Post, Comment
from user_app.models import CustomUser
from datetime import datetime

class TestUrls(SimpleTestCase):

    # Main
    def test_community_all_url(self):
        url = reverse("community_app:community", args=["all"])
        self.assertEquals(resolve(url).func, main.community)
    
    def test_community_follower_url(self):
        url = reverse("community_app:community", args=["follower"])
        self.assertEquals(resolve(url).func, main.community)


    # Post
    def test_post_create_url(self):
        url = reverse("community_app:post_create")
        self.assertEquals(resolve(url).func, post.create)

    def test_post_like_url(self):
        url = reverse("community_app:like_toggle", kwargs={"post_id": 1})
        self.assertEquals(resolve(url).func, post.like_toggle)

    def test_post_delete_url(self):
        url = reverse("community_app:post_delete", kwargs={"post_id": 1})
        self.assertEquals(resolve(url).func, post.delete)

    # Comment
    def test_comment_create_url(self):
        url = reverse("community_app:comment_create", kwargs={"post_id": 1})
        self.assertEquals(resolve(url).func, comment.create)
    
    def test_like_comment_url(self):
        url = reverse("community_app:like_comment", kwargs={"comment_id": 1})
        self.assertEquals(resolve(url).func, comment.like_comment)

    def test_comment_delete_url(self):
        url = reverse("community_app:comment_delete", kwargs={"comment_id": 1})
        self.assertEquals(resolve(url).func, comment.delete)
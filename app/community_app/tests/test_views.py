from django.test import TestCase, Client
from django.urls import reverse
from community_app.models import Post, PostLike, Comment, CommentLike
from user_app.models import CustomUser
from django.contrib.auth import get_user_model

class TestViews(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("test", "test@test.de", "test")
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_GET(self):
        
        response = self.client.get(reverse("community_app:community", args=["all"]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'community_app/community.html')

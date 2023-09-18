from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestViews(TestCase):

    #Test User erstellen und einloggen
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("test", "test@test.de", "test")
        self.client = Client()


    def test_inbox_page_unauthorized_html(self):
        response = self.client.get(reverse("messaging_app:inbox"))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url

    def test_inbox_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("messaging_app:inbox"))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'messaging_app/inbox.html')

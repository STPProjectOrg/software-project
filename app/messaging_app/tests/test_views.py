from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestViews(TestCase):

    #Test User erstellen und einloggen
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("test", "test@test.de", "test")
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_inbox_page_html(self):
        response = self.client.get(reverse("messaging_app:inbox"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging_app/inbox.html')

    #TODO kwargs müssen gefüllt werden
    '''
    def test_inbox_chat_page_html(self):
        response = self.client.get(reverse("messaging_app:inbox_chat", kwargs={"participant_req": ""}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging_app/inbox_chat.html')
    '''
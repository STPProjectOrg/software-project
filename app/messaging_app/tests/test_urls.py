from django.test import SimpleTestCase
from django.urls import reverse, resolve
from messaging_app.views import inbox


class TestUrls(SimpleTestCase):

    def test_inbox_url(self):
        url = reverse("messaging_app:inbox")
        self.assertEquals(resolve(url).func, inbox.inbox)
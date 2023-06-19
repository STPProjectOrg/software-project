from django.test import SimpleTestCase
from django.urls import reverse, resolve
from messaging_app.views import inbox, inbox_chat



class TestUrls(SimpleTestCase):

    def test_inbox_url(self):
        url = reverse("messaging_app:inbox")
        self.assertEquals(resolve(url).func, inbox)


    #TODO args müssen gefüllt werden, hans ist nicht in jeder datenbank hinterlegt als nutzer
    '''
    def test_inbox_chat_url(self):
        url = reverse("messaging_app:inbox-chat", args=["hans"])
        self.assertEquals(resolve(url).func, inbox_chat)
    '''
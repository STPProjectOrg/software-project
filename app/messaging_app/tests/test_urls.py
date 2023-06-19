from django.test import SimpleTestCase
from django.urls import reverse, resolve
from messaging_app.views import inbox, inbox_chat



class TestUrls(SimpleTestCase):

    def test_inbox_url(self):
        url = reverse("messaging_app:inbox")
        self.assertEquals(resolve(url).func, inbox)


    #TODO kwargs müssen gefüllt werden
    '''
    def test_inbox_chat_url(self):
        url = reverse("messaging_app:inbox_chat", kwargs={"participant_req": ""})
        self.assertEquals(resolve(url).func, inbox_chat)
    '''
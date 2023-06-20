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

    def test_dashboard_page_html(self):
        response = self.client.get(reverse("dashboard_app:dashboard"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_app/dashboard.html')

    ''' Stellt API-Anfrage
    def test_asset_page_html(self):
        response = self.client.get(reverse("dashboard_app:asset", kwargs={"coin": "btc"}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_app/asset.html')
    '''

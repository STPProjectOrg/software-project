from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestViews(TestCase):

    #Test User erstellen und einloggen
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("test", "test@test.de", "test")
        self.client = Client()


    def test_dashboard_page_unauthorized_html(self):
        response = self.client.get(reverse("dashboard_app:dashboard", kwargs={"timespan" : 0}))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url
   
    def test_dashboard_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("dashboard_app:dashboard", kwargs={"timespan" : 0}))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'dashboard_app/dashboard.html')

    def test_asset_page_unauthorized_html(self):
        response = self.client.get(reverse("dashboard_app:asset", args=["BTC",0]))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url

    '''Benötigt Asset in der Testdatenbank, vebraucht API-Anfrage
    def test_asset_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("dashboard_app:asset", args=["BTC",0]))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'dashboard_app/asset.html')
    '''
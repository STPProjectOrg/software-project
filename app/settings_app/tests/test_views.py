from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime

class TestViews(TestCase):

    #Test User erstellen und einloggen
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("test", "test@test.de", "test")
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_settings_page_html(self):
        response = self.client.get(reverse("settings_app:overview"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings_app/settingsOverview.html')

    def test_user_settings_page_html(self):
        response = self.client.get(reverse("settings_app:userSettings"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings_app/userSettings.html')

    def test_security_settings_page_html(self):
        response = self.client.get(reverse("settings_app:securitySettings"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings_app/securitySettings.html')


    def test_portfolio_settings_page_html(self):
        response = self.client.get(reverse("settings_app:portfolioSettings"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings_app/portfolioSettings.html')
    
    ''' TODO Post variante
    def test_portfolio_settings_page_html(self):
        response = self.client.post(reverse("settings_app:portfolioSettings"), {"dateTimeFormat": "", "currencySelector": ""}, )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings_app/settingsOverview.html')
    '''
    def test_notification_settings_page_html(self):
        response = self.client.get(reverse("settings_app:notificationSettings"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings_app/notificationSettings.html')
    
    def test_view_settings_page_html(self):
        response = self.client.get(reverse("settings_app:viewSettings"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings_app/viewSettings.html')
    
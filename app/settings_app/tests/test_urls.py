from django.test import SimpleTestCase
from django.urls import reverse, resolve
from settings_app.views import user_settings, security_settings, portfolio_settings, notification_settings, view_settings


class TestUrls(SimpleTestCase):

    def test_user_settings_url(self):
        url = reverse("settings_app:userSettings")
        self.assertEquals(resolve(url).func, user_settings)

    def test_security_settings_url(self):
        url = reverse("settings_app:securitySettings")
        self.assertEquals(resolve(url).func, security_settings)

    def test_portfolio_settings_url(self):
        url = reverse("settings_app:portfolioSettings")
        self.assertEquals(resolve(url).func, portfolio_settings)

    def test_view_settings_url(self):
        url = reverse("settings_app:viewSettings")
        self.assertEquals(resolve(url).func, view_settings)
    
    def test_notification_settings_url(self):
        url = reverse("settings_app:notificationSettings")
        self.assertEquals(resolve(url).func, notification_settings)
        

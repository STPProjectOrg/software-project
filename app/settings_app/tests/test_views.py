from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestViews(TestCase):

    #Test User erstellen und einloggen
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("test", "test@test.de", "test")
        self.client = Client()

    def test_settings_page_unauthorized_html(self):
        response = self.client.get(reverse("settings_app:overview"))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url

    def test_user_settings_page_unauthorized_html(self):
        response = self.client.get(reverse("settings_app:userSettings"))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url

    def test_security_settings_page_unauthorized_html(self):
        response = self.client.get(reverse("settings_app:securitySettings"))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url


    def test_portfolio_settings_page_unauthorized_html(self):
        response = self.client.get(reverse("settings_app:portfolioSettings"))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url
    
    ''' TODO Post variante
    def test_portfolio_settings_page_unauthorized_html(self):
        response = self.client.post(reverse("settings_app:portfolioSettings"), {"dateTimeFormat": "", "currencySelector": ""}, )

        self.assertEquals(response.status_code, 200)
        assert 'login' in response.url
    '''
    def test_notification_settings_page_unauthorized_html(self):
        response = self.client.get(reverse("settings_app:notificationSettings"))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url
    
    def test_view_settings_page_unauthorized_html(self):
        response = self.client.get(reverse("settings_app:viewSettings"))

        assert response.status_code == 302, 'Should redirect to login page'
        assert 'login' in response.url

    ### Authorized
    def test_settings_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("settings_app:overview"))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'settings_app/settingsOverview.html')

    def test_user_settings_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("settings_app:userSettings"))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'settings_app/userSettings.html')

    '''
    def test_security_settings_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("settings_app:securitySettings"))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'settings_app/securitySettings.html')
    	'''

    def test_portfolio_settings_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("settings_app:portfolioSettings"))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'settings_app/portfolioSettings.html')
    
    ''' TODO Post variante
    def test_portfolio_settings_page_authorized_html(self):
        response = self.client.post(reverse("settings_app:portfolioSettings"), {"dateTimeFormat": "", "currencySelector": ""}, )

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'settings_app/settingsOverview.html')
    '''
    def test_notification_settings_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("settings_app:notificationSettings"))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'settings_app/notificationSettings.html')
    
    def test_view_settings_page_authorized_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse("settings_app:viewSettings"))

        assert response.status_code == 200, 'Status code should be 200'
        self.assertTemplateUsed(response, 'settings_app/viewSettings.html')
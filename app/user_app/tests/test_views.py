from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from user_app.views import profile
from user_app.models import UserProfileInfo, CustomUser
from unittest.mock import patch

User = get_user_model()

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile = UserProfileInfo.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')

    @patch('user_app.views.profile.get_chart_data')
    @patch('community_app.views.post.get_by_user')
    def test_profile_view(self, mock_get_by_user, mock_get_chart_data):
        request = self.factory.get('/profile/testuser/7/')
        request.user = self.user

        mock_get_by_user.return_value = []
        mock_get_chart_data.return_value = {
            "assets": [],
            "pie_data": [],
            "line_data": [2, 4],
            "has_transactions": False,
            "kpi_total": 0,
            "anonymize": False,
        }

        response = profile.profile(request, 'testuser', 7)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile of testuser')
        self.assertTemplateUsed(response, 'user_app/profile.html')

        mock_get_by_user.assert_called_once_with(self.profile.user)
        mock_get_chart_data.assert_called_once_with(self.profile.user.id, self.profile.user.settings.dashboard_privacy_settings, 7)
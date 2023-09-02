from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_app.models import UserProfileInfo, ProfileBanner, UserFollowing
from community_app.models import Post
from community_app.forms import PostForm
from dashboard_app.models import Transaction
from api_app.models import Asset
from unittest.mock import patch

User = get_user_model()

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client_user = User.objects.create_user(
            username='client',
            email='test@example.com',
            password='testpassword'
        )
        self.other_user = User.objects.create_user(
            username='bob',
            email='test2@example.com',
            password='testpassword'
        )
        
        self.profile = UserProfileInfo.objects.create(user=self.client_user)
        self.profilebanner = ProfileBanner.objects.create(user=self.client_user)
        self.client.login(username='client', password='testpassword')

        UserFollowing.objects.create(
            follower_user=self.client_user, following_user=self.other_user)
        UserFollowing.objects.create(
            follower_user=self.other_user, following_user=self.client_user)
        
        Transaction.objects.create(
            user=self.client_user,
            asset=Asset.objects.create(name="BTC", coinName="Bitcoin"),
            purchaseDate=datetime.now(),
            amount=10.0,
            price=100.0,
            tax=5.0,
            charge=2.0,
            cost=1000.0,
        )


    def test_profile_view(self):
        url = reverse('user_app:profile', args=[self.client_user.username, 7])
        mock_data = self.create_mock_data()

        with patch('community_app.views.post.get_by_user') as mock_get_by_user, \
                patch('dashboard_app.views.kpi.get_kpi') as mock_get_kpi, \
                patch('dashboard_app.views.charts.get_pie_data') as mock_get_pie_data, \
                patch('dashboard_app.views.charts.get_portfolio_line_data') as mock_get_line_data:

            mock_get_by_user.return_value = mock_data["mock_get_by_user"]
            mock_get_kpi.return_value = mock_data["mock_get_kpi"]
            mock_get_pie_data.return_value = mock_data["mock_get_pie_data"]
            mock_get_line_data.return_value = mock_data["mock_get_line_data"]

            response = self.client.get(url)

        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_app/profile.html')
        self.assertEqual(context['profile_user'], self.client_user)
        self.assertEqual(context['user_profile_id'], self.client_user.userprofileinfo.id)
        self.assertEqual(context['is_user_profile'], True)
        self.assertEqual(context['portfolio_privacy_setting'], 'all')
        self.assertQuerysetEqual(context['profile_followers_list'], [self.other_user])
        self.assertQuerysetEqual(context['profile_following_list'], [self.other_user])
        self.assertEqual(context['is_user_following'], False)
        self.assertIsInstance(context['postform'], PostForm)
        self.assertQuerysetEqual(context['myposts'], mock_get_by_user.return_value)
        self.assertEqual(context['kpi_total'], mock_get_kpi.return_value['total'])
        self.assertEqual(context['pie_data'], mock_get_pie_data.return_value)
        self.assertEqual(context['line_data'], mock_get_line_data.return_value)
        self.assertEqual(context['has_transactions'], True)
        

    def create_mock_data(self):
        return {
            "mock_get_by_user": [Post.objects.create(
                user=self.client_user,
                content="content",
                created_at=datetime.now(),
                tags="tag"
            )],
            "mock_get_kpi": {'total': 200},
            "mock_get_pie_data": {
                'data': [199328.32],
                'labels': ['Bitcoin'],
                'symbols': ['BTC']
            },
            "mock_get_line_data": {
                'button_values': {'1week': 0.007, '1month': 14.02, '6month': 14.22, '1year': 14.22, 'all': 14.22},
                'data': [13975.92],
                'labels': ['13.04.2023']
            }
        }
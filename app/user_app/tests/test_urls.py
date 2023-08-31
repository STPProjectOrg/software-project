from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_app.views import register, profile_redirect, profile, ProfilePicUpdateView, delete_profile_pic, toggle_follow, follower_list


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_app.models import UserProfileInfo, ProfileBanner, UserFollowing

User = get_user_model()

class UserAppUrlsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.profile = UserProfileInfo.objects.create(user=self.user)
        self.banner = ProfileBanner.objects.create(user=self.user)
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )

    def test_profile_redirect(self):
        response = self.client.get(reverse('user_app:profile_redirect'))
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.get(reverse('user_app:profile', args=['testuser', 0]))
        self.assertEqual(response.status_code, 200)

    def test_follow(self):
        response = self.client.get(reverse('user_app:follow', args=['otheruser']))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_update_userprofile(self):
        response = self.client.get(reverse('user_app:update_userprofile', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_userbanner(self):
        response = self.client.get(reverse('user_app:update_userbanner', args=[self.banner.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_biography(self):
        response = self.client.get(reverse('user_app:update_biography'))
        self.assertEqual(response.status_code, 200)

    def test_delete_userprofile(self):
        response = self.client.get(reverse('user_app:delete_userprofile', args=[self.profile.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_register(self):
        response = self.client.get(reverse('user_app:register'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('user_app:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('user_app:logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_reset_password(self):
        response = self.client.get(reverse('user_app:reset_password'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done(self):
        response = self.client.get(reverse('user_app:password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm(self):
        uidb64 = 'd9ad5f5c1b4f4faa94d141c2cc587534'
        token = '3y6-99442d3e496bf687e166'
        response = self.client.get(reverse('user_app:password_reset_confirm', args=[uidb64, token]))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete(self):
        response = self.client.get(reverse('user_app:password_reset_complete'))
        self.assertEqual(response.status_code, 200)

# class TestUrls(SimpleTestCase):

#     def test_register_url(self):
#         url = reverse("user_app:register")
#         self.assertEquals(resolve(url).func, register)

#     '''
#     def test_login_url(self):
#         url = reverse("user_app:register")
#         self.assertEquals(resolve(url).func, register)
#     def test_logout_url(self):
#         url = reverse("user_app:register")
#         self.assertEquals(resolve(url).func, register)
#     '''
    
#     def test_profile_redirect_url(self):
#         url = reverse("user_app:profile_redirect")
#         self.assertEquals(resolve(url).func, profile_redirect)

#     ''' TODO Args 
#     def test_profile_url(self):
#         url = reverse("user_app:profile", args=[""])
#         self.assertEquals(resolve(url).func, profile)

#     def test_update_userprofile_url(self):
#         url = reverse("user_app:update_userprofile", args=[""])
#         self.assertEquals(resolve(url).func, ProfilePicUpdateView.as_view())

#     def test_delete_profile_pic_url(self):
#         url = reverse("user_app:delete/userprofile", args=[""])
#         self.assertEquals(resolve(url).func, delete_profile_pic)

#     def test_follow_url(self):
#         url = reverse("user_app:follow", args=[""])
#         self.assertEquals(resolve(url).func, toggle_follow)

#     def test_follower_list_url(self):
#         url = reverse("user_app:follower_list", args=[""])
#         self.assertEquals(resolve(url).func, follower_list)
#     '''

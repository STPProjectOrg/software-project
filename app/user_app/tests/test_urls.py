from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_app.views import register, profile_redirect, profile, ProfilePicUpdateView, delete_profile_pic, toggle_follow, follower_list


class TestUrls(SimpleTestCase):

    def test_register_url(self):
        url = reverse("user_app:register")
        self.assertEquals(resolve(url).func, register)

    '''
    def test_login_url(self):
        url = reverse("user_app:register")
        self.assertEquals(resolve(url).func, register)
    def test_logout_url(self):
        url = reverse("user_app:register")
        self.assertEquals(resolve(url).func, register)
    '''
    
    def test_profile_redirect_url(self):
        url = reverse("user_app:profile_redirect")
        self.assertEquals(resolve(url).func, profile_redirect)

    ''' TODO Args 
    def test_profile_url(self):
        url = reverse("user_app:profile", args=[""])
        self.assertEquals(resolve(url).func, profile)

    def test_update_userprofile_url(self):
        url = reverse("user_app:update_userprofile", args=[""])
        self.assertEquals(resolve(url).func, ProfilePicUpdateView.as_view())

    def test_delete_profile_pic_url(self):
        url = reverse("user_app:delete/userprofile", args=[""])
        self.assertEquals(resolve(url).func, delete_profile_pic)

    def test_follow_url(self):
        url = reverse("user_app:follow", args=[""])
        self.assertEquals(resolve(url).func, toggle_follow)

    def test_follower_list_url(self):
        url = reverse("user_app:follower_list", args=[""])
        self.assertEquals(resolve(url).func, follower_list)
    '''

import sys
import pytest
import os
from django.test import TestCase
from mixer.backend.django import mixer
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from user_app.models import CustomUser, UserFollowing, ProfileBanner, UserProfileInfo
from PIL import Image

pytestmark = pytest.mark.django_db
User = get_user_model()

class TestModelInstances(TestCase):
    """
    Test cases to verify the creation of model instances using mixer.
    """
    def test_custom_user(self):
        CustomUser = mixer.blend('user_app.CustomUser')
        assert CustomUser.pk == 1, 'Should create a CustomUser instance'

    def test_user_following(self):
        UserFollowing = mixer.blend('user_app.UserFollowing')
        assert UserFollowing.pk == 1, 'Should create a UserFollowing instance'
    
    def test_user_profile_info(self):
        UserProfileInfo = mixer.blend('user_app.UserProfileInfo')
        assert UserProfileInfo.pk == 1, 'Should create a UserProfileInfo instance'

    def test_user_profile_banner(self):
        UserProfileBanner = mixer.blend('user_app.ProfileBanner')
        assert UserProfileBanner.pk == 1, 'Should create a ProfileBanner instance'


class CustomUserModelTest(TestCase):
    """
    Test cases for the CustomUser model.
    """
    
    def setUp(self):
        """
        Set up a test user for the test cases.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword'
        )

    def test_create_user(self):
        """
        Test case to create a user instance and validate its attributes.
        """
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User') 
        self.assertFalse(self.user.ws_state)

    def test_user_str(self):
        """
        Test case to validate the string representation of the user.
        """
        self.assertEqual(str(self.user), 'testuser')


class UserFollowingModelTest(TestCase):
    """
        Set up users and create a following relationship for testing.
    """
    
    def setUp(self):
        """
        Set up users and create a following relationship for testing.
        """
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpassword1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpassword2'
        )
        UserFollowing.objects.create(
            follower_user=self.user1,
            following_user=self.user2
        )

    def test_following_and_followers_query(self):
        """
        Test case to validate following and followers relationships.
        """
        user1 = CustomUser.objects.get(username='user1')
        user2 = CustomUser.objects.get(username='user2')

        following_users = user1.following.all()
        followers_users = user2.followers.all()

        self.assertEqual(following_users.count(), 1)
        self.assertEqual(followers_users.count(), 1)

        following_user = following_users.first()
        followers_user = followers_users.first()

        self.assertEqual(following_user.following_user, user2)
        self.assertEqual(followers_user.follower_user, user1)


class ProfileBannerModelTest(TestCase):
    """
    Test cases for the ProfileBanner model.
    """

    def setUp(self):
        """
        Set up a user for testing.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_profile_banner_creation(self):
        """
        Test case to ensure correct creation of a ProfileBanner instance.
        """
        banner = ProfileBanner.objects.create(user=self.user)
        self.assertEqual(banner.user, self.user)
        self.assertEqual(banner.profile_banner, ProfileBanner.BannerChoices.BANNER_1)
    
    def test_get_banner_choices(self):
        """
        Test case to validate the available banner choices.
        """
        banner = ProfileBanner.objects.create(user=self.user)
        choices = banner.get_banner_choices()
        self.assertEqual(choices, [
            (ProfileBanner.BannerChoices.BANNER_1, 'Banner 1'),
            (ProfileBanner.BannerChoices.BANNER_2, 'Banner 2'),
            (ProfileBanner.BannerChoices.BANNER_3, 'Banner 3'),
            (ProfileBanner.BannerChoices.BANNER_4, 'Banner 4'),
        ])
    
    def test_get_profile_banner(self):
        """
        Test case to ensure correct retrieval of the profile banner choice.
        """
        banner = ProfileBanner.objects.create(user=self.user)
        self.assertEqual(banner.get_profile_banner(), ProfileBanner.BannerChoices.BANNER_1)
    
    def test_change_profile_banner(self):
        """
        Test case to validate changing the profile banner choice.
        """
        banner = ProfileBanner.objects.create(user=self.user)
        banner.profile_banner = ProfileBanner.BannerChoices.BANNER_2
        banner.save()
        self.assertEqual(banner.get_profile_banner(), ProfileBanner.BannerChoices.BANNER_2)


class UserProfileInfoModelTest(TestCase):
    """
    Test cases for the UserProfileInfo model.
    """

    def setUp(self):
        """
        Set up a user and a test image for testing.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpeg')
        with open(test_image_path, 'rb') as f:
            self.test_image = SimpleUploadedFile(
                name='test_image.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
    
    def test_profile_pic_default(self):
        """
        Test case to ensure default profile picture URL is set correctly.
        """
        profile_info = UserProfileInfo.objects.create(user=self.user)
        self.assertEqual(profile_info.get_profile_pic(), settings.DEFAULT_IMAGE_URL)
    
    def test_profile_pic_custom(self):
        """
        Test case to verify the correct setting of a custom profile picture.
        """
        profile_info = UserProfileInfo.objects.create(user=self.user, profile_pic=self.test_image)
        self.assertEqual(profile_info.profile_pic.url, "/media/profile_pics/test_image.jpg")

    def test_resize_profile_pic(self):
        """
        Test case to confirm that a profile picture is resized if necessary.
        """
        profile_info = UserProfileInfo.objects.create(user=self.user, profile_pic=self.test_image)
        resized_image = Image.open(profile_info.profile_pic.path)
        self.assertLessEqual(resized_image.height, 300)
        self.assertLessEqual(resized_image.width, 300)

    def tearDown(self):
        """
        Clean up the media directory after tests if necessary.
        """
        if 'test' in sys.argv:
            import shutil
            shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

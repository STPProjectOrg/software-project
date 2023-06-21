import pytest
from django.test import TestCase
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestModel(TestCase):
    def test_custom_user(self):
        CustomUser = mixer.blend('user_app.CustomUser')
        assert CustomUser.pk == 1, 'Should create a CustomUser instance'

    def test_user_following(self):
        UserFollowing = mixer.blend('user_app.UserFollowing')
        assert UserFollowing.pk == 1, 'Should create a UserFollowing instance'
    
    def test_user_profile_info(self):
        UserProfileInfo = mixer.blend('user_app.UserProfileInfo')
        assert UserProfileInfo.pk == 1, 'Should create a UserProfileInfo instance'
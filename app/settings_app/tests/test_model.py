import pytest
from django.test import TestCase
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestModel(TestCase):
    def test_settings(self):
        settings = mixer.blend('settings_app.Settings')
        assert settings.pk == 1, 'Should create a Settings instance'

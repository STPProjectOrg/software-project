import pytest
from django.test import TestCase
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestModel(TestCase):
    def test_transaction(self):
        transaction = mixer.blend('dashboard_app.Transaction')
        assert transaction.pk == 1, 'Should create a Tranaction instance'

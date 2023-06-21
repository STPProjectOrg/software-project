import pytest
from django.test import TestCase
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestModel(TestCase):
    def test_inbox(self):
        inbox = mixer.blend('messaging_app.Inbox')
        assert inbox.pk == 1, 'Should create a Inbox instance'

    def test_inbox_participants(self):
        inbox_participants = mixer.blend('messaging_app.InboxParticipants')
        assert inbox_participants.pk == 1, 'Should create a InboxParticipants instance'
    
    def test_message(self):
        message = mixer.blend('messaging_app.Message')
        assert message.pk == 1, 'Should create a Message instance'
import pytest
from django.test import TestCase
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestModel(TestCase):
    def test_post(self):
        post = mixer.blend('community_app.Post')
        assert post.pk == 1, 'Should create a Post instance'

    def test_post_like(self):
        post_like = mixer.blend('community_app.PostLike')
        assert post_like.pk == 1, 'Should create a PostLike instance'
    
    def test_comment(self):
        comment = mixer.blend('community_app.Comment')
        assert comment.pk == 1, 'Should create a Comment instance'

    def test_comment_like(self):
        comment_like = mixer.blend('community_app.CommentLike')
        assert comment_like.pk == 1, 'Should create a CommentLike instance'

    def test_tag(self):
        tag = mixer.blend('community_app.Tag')
        assert tag.pk == 1, 'Should create a Tag instance'
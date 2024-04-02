from django.contrib.auth import get_user_model
from django.test import Client


User = get_user_model()


class AuthorMixin:
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

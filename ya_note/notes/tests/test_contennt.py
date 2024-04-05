from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note
from notes.tests.test_routes import User
from .mixins import AuthorMixin


class TestContent(AuthorMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_logged = Client()
        cls.reader_logged.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.URL_NOTES_LIST = reverse('notes:list')
        cls.URL_NOTES_ADD = reverse('notes:add')
        cls.URL_NOTES_EDIT = reverse('notes:edit', args=(cls.note.slug,))

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.reader_logged, False),
        )
        for user, status in users_statuses:
            with self.subTest():
                response = user.get(self.URL_NOTES_LIST)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, status)

    def test_pages_contain_form(self):
        urls = (self.URL_NOTES_ADD, self.URL_NOTES_EDIT)
        for url in urls:
            with self.subTest():
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertTrue(isinstance(response.context['form'], NoteForm))

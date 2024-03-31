from http import HTTPStatus

from django.contrib.auth import get_user_model

from django.test import Client
from django.test import TestCase

from django.urls import reverse

from pytils.translit import slugify

from notes.forms import WARNING

from notes.models import Note

User = get_user_model()


class AuthorMixin:
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)


class TestNoteCreation(AuthorMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.add_url = reverse('notes:add')
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': 'slug',
        }

    def test_user_can_create_note(self):
        initial_notes_count = Note.objects.count()
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        final_notes_count = Note.objects.count()
        self.assertEqual(final_notes_count, initial_notes_count + 1)

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.add_url, data=self.form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={self.add_url}'
        self.assertRedirects(response, expected_url)
        notes_count = Note.objects.count()
        expected_count = 0
        self.assertEqual(notes_count, expected_count)

    def test_not_unique_slug(self):
        self.author_client.post(self.add_url, data=self.form_data)
        response = self.author_client.post(self.add_url, data=self.form_data)
        warning = self.form_data['slug'] + WARNING
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=warning
        )

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        expected_count = 1
        self.assertEqual(notes_count, expected_count)
        expected_slug = slugify(self.form_data['title'])
        note_slug = Note.objects.get(slug=expected_slug)
        self.assertEqual(note_slug.slug, expected_slug)


class TestNoteEditDelete(AuthorMixin, TestCase):
    NEW_NOTE_TITLE = 'Новый заголовок'
    NEW_NOTE_TEXT = 'Новый текст'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
        }
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author,

        )
        cls.edit_note = reverse('notes:edit', args=[cls.note.slug])
        cls.delete_note = reverse('notes:delete', args=[cls.note.slug])

    def test_author_can_edit_note(self):
        self.author_client.post(self.edit_note, self.form_data)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NEW_NOTE_TITLE)
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(self.edit_note, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)

    def test_author_can_delete_note(self):
        response = self.author_client.post(self.delete_note, self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        expected_count = 0
        self.assertEqual(notes_count, expected_count)

    def test_other_user_cant_delete_note(self):
        response = self.reader_client.post(self.delete_note, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        expected_count = 1
        self.assertEqual(notes_count, expected_count)

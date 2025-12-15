from books.models import Author
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class TestAuthorModel(TestCase):

    def test_create_author_successfully(self):
        author = Author.objects.create(name="J.K. Rowling", biography="Author of Harry Potter")

        self.assertEqual(author.name, "J.K. Rowling")
        self.assertEqual(author.biography, "Author of Harry Potter")
        self.assertIsNotNone(author.datetime_created)

    def test_name_max_length_validation(self):
        long_name = "a" * 256
        author = Author(name=long_name)

        with self.assertRaises(ValidationError):
            author.full_clean()

    def test_name_must_be_unique(self):
        Author.objects.create(name="Tolkien")

        with self.assertRaises(IntegrityError):
            Author.objects.create(name="Tolkien")

    def test_biography_can_be_blank(self):
        author = Author.objects.create(name="George Orwell", biography="")
        self.assertEqual(author.biography, "")

    def test_str_method_returns_name(self):
        author = Author.objects.create(name="Str Test")
        self.assertEqual(str(author), "Str Test")

from books.models import ContentFormat
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class TestContentFormatModel(TestCase):

    def test_create_content_format_successfully(self):
        fmt = ContentFormat.objects.create(name="Audio")
        self.assertEqual(fmt.name, "Audio")

    def test_name_max_length_validation(self):
        long_name = "a" * 51
        fmt = ContentFormat(name=long_name)

        with self.assertRaises(ValidationError):
            fmt.full_clean()

    def test_name_must_be_unique(self):
        ContentFormat.objects.create(name="Ebook")

        with self.assertRaises(IntegrityError):
            ContentFormat.objects.create(name="Ebook")

    def test_str_method_returns_name(self):
        fmt = ContentFormat.objects.create(name="Str Test")
        self.assertEqual(str(fmt), "Str Test")

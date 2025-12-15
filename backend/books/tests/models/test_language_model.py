from books.models import Language
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class TestLanguageModel(TestCase):

    def test_create_language_successfully(self):
        lang = Language.objects.create(name="English")

        self.assertEqual(lang.name, "English")

    def test_name_max_length_validation(self):
        long_name = "a" * 51
        lang = Language(name=long_name)

        with self.assertRaises(ValidationError):
            lang.full_clean()

    def test_name_must_be_unique(self):
        Language.objects.create(name="Persian")

        with self.assertRaises(IntegrityError):
            Language.objects.create(name="Persian")

    def test_str_method_returns_name(self):
        lang = Language.objects.create(name="Str Test")

        self.assertEqual(str(lang), "Str Test")

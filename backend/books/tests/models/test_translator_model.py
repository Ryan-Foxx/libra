from books.models import Translator
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class TestTranslatorModel(TestCase):

    def test_create_translator_successfully(self):
        translator = Translator.objects.create(name="Translator One", about="Experienced translator.")
        self.assertEqual(translator.name, "Translator One")
        self.assertEqual(translator.about, "Experienced translator.")
        self.assertIsNotNone(translator.datetime_created)

    def test_name_max_length_validation(self):
        long_name = "a" * 256
        translator = Translator(name=long_name)

        with self.assertRaises(ValidationError):
            translator.full_clean()

    def test_name_must_be_unique(self):
        Translator.objects.create(name="UniqueTest")

        with self.assertRaises(IntegrityError):
            Translator.objects.create(name="UniqueTest")

    def test_name_can_be_blank(self):
        translator = Translator.objects.create(name="", about="Some info")
        self.assertEqual(translator.name, "")

    def test_unique_blank_name_allowed_once(self):
        Translator.objects.create(name="")

        with self.assertRaises(IntegrityError):
            Translator.objects.create(name="")

    def test_about_can_be_blank(self):
        translator = Translator.objects.create(name="John", about="")
        self.assertEqual(translator.about, "")

    def test_str_method_returns_name(self):
        translator = Translator.objects.create(name="Str Test")
        self.assertEqual(str(translator), "Str Test")

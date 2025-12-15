from books.models import Publisher
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class TestPublisherModelTest(TestCase):

    def test_create_publisher_successfully(self):
        publisher = Publisher.objects.create(name="O'Reilly Media", about="Technology publisher")

        self.assertEqual(publisher.name, "O'Reilly Media")
        self.assertEqual(publisher.about, "Technology publisher")
        self.assertIsNotNone(publisher.datetime_created)

    def test_name_max_length_validation(self):
        long_name = "a" * 256
        publisher = Publisher(name=long_name)

        with self.assertRaises(ValidationError):
            publisher.full_clean()

    def test_name_must_be_unique(self):
        Publisher.objects.create(name="HarperCollins")

        with self.assertRaises(IntegrityError):
            Publisher.objects.create(name="HarperCollins")

    def test_about_can_be_blank(self):
        publisher = Publisher.objects.create(name="Penguin Books", about="")
        self.assertEqual(publisher.about, "")

    def test_str_method_returns_name(self):
        publisher = Publisher.objects.create(name="Str Test")
        self.assertEqual(str(publisher), "Str Test")

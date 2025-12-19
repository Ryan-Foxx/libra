import os
import tempfile
from datetime import date, timedelta

from books.models import Book, Category, Publisher
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestBookCoverImageModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher = Publisher.objects.create(name="Pub A")
        cls.category = Category.objects.create(title="Cat A")

    def get_test_image(self, name="cover.jpg"):
        return SimpleUploadedFile(
            name=name,
            content=b"\x47\x49\x46\x38\x39\x61",
            content_type="image/jpeg",
        )

    def _create_book(self, **kwargs):
        data = {
            "name": "Test Book",
            "description": "desc",
            "publisher": self.publisher,
            "category": self.category,
            "volume": 1,
            "number_of_pages": 10,
            "approximate_study_time": timedelta(days=10, hours=5, minutes=30, seconds=10),
            "publication_date": date(2020, 5, 12),
        }
        data.update(kwargs)
        return Book.objects.create(**data)

    def test_cover_image_can_be_null(self):

        book = self._create_book()
        self.assertFalse(book.cover_image)

    def test_cover_image_saved_correctly(self):

        book = self._create_book(cover_image=self.get_test_image())

        self.assertTrue(book.cover_image)
        self.assertTrue(book.cover_image.name.startswith("books/covers/"))

    def test_clearing_cover_image_does_not_delete_file_from_disk(self):

        book = self._create_book(cover_image=self.get_test_image("first.jpg"))

        file_path = book.cover_image.path
        self.assertTrue(os.path.exists(file_path))

        book.cover_image = None
        book.save()

        self.assertFalse(book.cover_image)
        self.assertIsNone(book.cover_image.name)

        self.assertTrue(
            os.path.exists(file_path),
            "Image file should still exist on disk after clearing field",
        )

    def test_replacing_cover_image_does_not_remove_old_file(self):

        book = self._create_book(cover_image=self.get_test_image("old.jpg"))
        old_path = book.cover_image.path
        self.assertTrue(os.path.exists(old_path))

        # replace image
        book.cover_image = self.get_test_image("new.jpg")
        book.save()

        new_path = book.cover_image.path

        self.assertTrue(os.path.exists(new_path))
        self.assertTrue(
            os.path.exists(old_path),
            "Old image file should still exist on disk after replacement",
        )

    def test_cover_image_field_definition(self):

        field = Book._meta.get_field("cover_image")

        self.assertEqual(field.upload_to, "books/covers/")
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

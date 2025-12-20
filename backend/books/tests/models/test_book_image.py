import os
import tempfile
from datetime import date

from books.models import Book, BookImage, Category, Publisher
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestBookImageModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher = Publisher.objects.create(name="Pub A")
        cls.category = Category.objects.create(title="Cat A")

        cls.book = Book.objects.create(
            name="Test Book",
            description="desc",
            publisher=cls.publisher,
            category=cls.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time="01:00:00",
            publication_date=date.today(),
        )

    def get_test_image(self, name="image.jpg"):
        return SimpleUploadedFile(
            name=name,
            content=b"\x47\x49\x46\x38\x39\x61",
            content_type="image/jpeg",
        )

    def _create_book_image(self, **kwargs):
        data = {
            "book": self.book,
            "description": "desc",
        }
        data.update(kwargs)
        return BookImage.objects.create(**data)

    def test_image_is_renamed_after_save(self):

        image = self._create_book_image(image=self.get_test_image("sample.jpg"))

        self.assertTrue(image.image)
        self.assertTrue(image.image.name.startswith("books/images/"))
        self.assertIn(
            f"{self.book.id}_{image.id}",
            image.image.name,
        )
        self.assertTrue(image.image.name.endswith(".jpg"))
        self.assertTrue(os.path.exists(image.image.path))

    def test_replacing_image_overwrites_file_without_duplicates(self):

        image = self._create_book_image(image=self.get_test_image("old.jpg"))

        first_path = image.image.path
        self.assertTrue(os.path.exists(first_path))

        image.image = self.get_test_image("new.jpg")
        image.save()

        image.refresh_from_db()
        second_path = image.image.path

        self.assertEqual(first_path, second_path)

        self.assertTrue(os.path.exists(second_path))

        images_dir = os.path.dirname(second_path)
        temp_files = [f for f in os.listdir(images_dir) if f.startswith("temp_")]

        self.assertEqual(
            temp_files,
            [],
            "Temporary image files should not remain after replace",
        )

    def test_clearing_image_deletes_file_from_disk(self):

        image = self._create_book_image(image=self.get_test_image("clear.jpg"))

        file_path = image.image.path
        self.assertTrue(os.path.exists(file_path))

        image.image = None
        image.save()

        self.assertFalse(image.image)
        self.assertFalse(
            os.path.exists(file_path),
            "Image file should be deleted after clearing field",
        )

    def test_deleting_book_image_deletes_file_from_disk(self):

        image = self._create_book_image(image=self.get_test_image("delete.jpg"))

        file_path = image.image.path
        self.assertTrue(os.path.exists(file_path))

        image.delete()

        self.assertFalse(
            os.path.exists(file_path),
            "Image file should be deleted after BookImage deletion",
        )

    def test_image_field_definition(self):

        field = BookImage._meta.get_field("image")

        self.assertTrue(field.null)
        self.assertTrue(field.blank)

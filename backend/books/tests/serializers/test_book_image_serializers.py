import tempfile
from datetime import date

from books.models import Book, BookImage, Category, Publisher
from books.serializers.book_image_serializers import BookImageSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestBookImageSerializer(TestCase):

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

    def get_test_image(self):
        return SimpleUploadedFile(
            name="image.jpg",
            content=b"\x47\x49\x46\x38\x39\x61",
            content_type="image/jpeg",
        )

    def test_book_image_serializer_fields(self):
        image = BookImage.objects.create(
            book=self.book,
            image=self.get_test_image(),
            description="Sample image",
        )

        serializer = BookImageSerializer(image)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"id", "image", "description"})

    def test_book_image_serializer_image_is_url(self):
        image = BookImage.objects.create(
            book=self.book,
            image=self.get_test_image(),
        )

        serializer = BookImageSerializer(image)
        data = serializer.data

        self.assertIsInstance(data["image"], str)
        self.assertTrue(data["image"].startswith("/media/books/images/"))

    def test_book_image_serializer_description(self):
        image = BookImage.objects.create(
            book=self.book,
            image=self.get_test_image(),
            description="Extra image",
        )

        serializer = BookImageSerializer(image)
        data = serializer.data

        self.assertEqual(data["description"], "Extra image")

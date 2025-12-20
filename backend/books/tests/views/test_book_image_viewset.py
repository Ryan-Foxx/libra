import tempfile
from datetime import date

from books.models import Book, BookImage, Category, Publisher
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestBookImageViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher = Publisher.objects.create(name="Pub A")
        cls.category = Category.objects.create(title="Cat A")

        cls.book1 = Book.objects.create(
            name="Book One",
            description="desc",
            publisher=cls.publisher,
            category=cls.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time="01:00:00",
            publication_date=date.today(),
        )

        cls.book2 = Book.objects.create(
            name="Book Two",
            description="desc",
            publisher=cls.publisher,
            category=cls.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time="01:00:00",
            publication_date=date.today(),
        )

    def get_test_image(self, name):
        return SimpleUploadedFile(
            name=name,
            content=b"\x47\x49\x46\x38\x39\x61",
            content_type="image/jpeg",
        )

    def test_list_images_for_book(self):
        BookImage.objects.create(
            book=self.book1,
            image=self.get_test_image("a.jpg"),
            description="Image A",
        )
        BookImage.objects.create(
            book=self.book1,
            image=self.get_test_image("b.jpg"),
            description="Image B",
        )

        url = reverse("book-images-list", kwargs={"book_pk": self.book1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_images_are_filtered_by_book(self):
        BookImage.objects.create(
            book=self.book1,
            image=self.get_test_image("book1.jpg"),
            description="Book 1 image",
        )

        BookImage.objects.create(
            book=self.book2,
            image=self.get_test_image("book2.jpg"),
            description="Book 2 image",
        )

        url = reverse("book-images-list", kwargs={"book_pk": self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        image_data = response.data[0]

        self.assertEqual(set(image_data.keys()), {"id", "image", "description"})
        self.assertIn("/media/books/images/", image_data["image"])
        self.assertEqual(image_data["description"], "Book 1 image")

    def test_empty_image_list_for_book_without_images(self):
        url = reverse("book-images-list", kwargs={"book_pk": self.book1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_response_structure(self):
        BookImage.objects.create(
            book=self.book1,
            image=self.get_test_image("cover.jpg"),
            description="Cover",
        )

        url = reverse("book-images-list", kwargs={"book_pk": self.book1.id})
        response = self.client.get(url)

        item = response.data[0]

        self.assertEqual(
            set(item.keys()),
            {"id", "image", "description"},
        )

    def test_non_existing_book_returns_empty_list(self):
        url = reverse("book-images-list", kwargs={"book_pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

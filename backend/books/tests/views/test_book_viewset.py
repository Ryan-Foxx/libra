from datetime import date, timedelta

from books.models import Book, Category, Publisher
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestBookViewSetReadOnly(APITestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Publisher A")
        self.category = Category.objects.create(title="Category A")

        self.book = Book.objects.create(
            name="Book A",
            description="Desc",
            publisher=self.publisher,
            category=self.category,
            price=100,
            active=False,
            volume=10,
            number_of_pages=100,
            approximate_study_time=timedelta(days=10, hours=5, minutes=30, seconds=10),
            publication_date=date(2024, 1, 1),
        )

    def test_post_is_not_allowed(self):
        url = reverse("book-list")
        response = self.client.post(url, data={"name": "X"})

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "POST should not be allowed on BookViewSet (read-only)",
        )

    def test_put_is_not_allowed(self):
        url = reverse("book-detail", args=[self.book.pk])
        response = self.client.put(url, data={"name": "X"})

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "PUT should not be allowed on BookViewSet (read-only)",
        )

    def test_patch_is_not_allowed(self):
        url = reverse("book-detail", args=[self.book.pk])
        response = self.client.patch(url, data={"name": "X"})

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "PATCH should not be allowed on BookViewSet (read-only)",
        )

    def test_delete_is_not_allowed(self):
        url = reverse("book-detail", args=[self.book.pk])
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "DELETE should not be allowed on BookViewSet (read-only)",
        )

    def test_allow_header_only_contains_safe_methods(self):
        url = reverse("book-detail", args=[self.book.pk])
        response = self.client.options(url)
        allowed_methods = set(response.headers.get("Allow").split(", "))

        self.assertSetEqual(
            allowed_methods,
            {"GET", "HEAD", "OPTIONS"},
            "BookViewSet should only allow safe HTTP methods",
        )

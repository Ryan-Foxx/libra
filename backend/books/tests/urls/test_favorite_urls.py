from datetime import date, timedelta

from books.models import Book, Category, Publisher
from books.views import FavoriteViewSet
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class TestFavoriteUrls(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="jack",
            email="user@test.com",
            password="password123",
        )

        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.category = Category.objects.create(title="Test Category")

        self.book = Book.objects.create(
            name="Test Book",
            description="Test description",
            price=1000,
            publisher=self.publisher,
            category=self.category,
            volume=10,
            number_of_pages=100,
            approximate_study_time=timedelta(days=10, hours=5, minutes=30, seconds=10),
            publication_date=date(2020, 5, 12),
        )
        self.url = reverse("favorite-list")

    def test_favorite_list_url_resolves(self):
        url = reverse("favorite-list")
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, FavoriteViewSet)

    def test_favorite_detail_url_resolves(self):
        url = reverse("favorite-detail", kwargs={"pk": 1})
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, FavoriteViewSet)

    def test_favorite_url_requires_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_favorite_allowed_methods(self):
        self.client.force_authenticate(user=self.user)

        # GET allowed
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

        # POST allowed
        response = self.client.post(self.url, {"book": self.book.id})
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT])

        # PUT not allowed
        response = self.client.put(self.url, {"book": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH not allowed
        response = self.client.patch(self.url, {"book": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # DELETE not allowed
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

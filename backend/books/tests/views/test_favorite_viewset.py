from datetime import date, timedelta

from books.models import Book, Category, Favorite, Publisher
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class FavoriteToggleTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="jack",
            email="user@test.com",
            password="password123",
            phone_number="+10000000001",
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

        self.url = "/api/favorites/"

    def test_toggle_creates_favorite_if_not_exists(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"book": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorite.objects.filter(user=self.user, book=self.book).exists())

    def test_toggle_deletes_favorite_if_exists(self):
        self.client.force_authenticate(user=self.user)

        Favorite.objects.create(user=self.user, book=self.book)
        self.assertEqual(Favorite.objects.filter(user=self.user, book=self.book).count(), 1)

        response = self.client.post(self.url, {"book": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorite.objects.filter(user=self.user, book=self.book).exists())

    def test_user_cannot_toggle_other_users_favorites(self):
        other_user = User.objects.create_user(
            username="other",
            password="password123",
            phone_number="+10000000002",
        )

        Favorite.objects.create(user=other_user, book=self.book)
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {"book": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Favorite.objects.filter(user=other_user, book=self.book).exists())
        self.assertTrue(Favorite.objects.filter(user=self.user, book=self.book).exists())

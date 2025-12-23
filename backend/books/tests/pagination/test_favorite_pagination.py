from datetime import date, timedelta

from books.models import Book, Category, Favorite, Publisher
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class TestFavoritePagination(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="jack",
            email="jack@test.com",
            password="password123",
            phone_number="+10000000001",
        )
        self.client.force_authenticate(user=self.user)

        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.category = Category.objects.create(title="Test Category")

        self.books = []
        for i in range(12):
            book = Book.objects.create(
                name=f"Book {i+1}",
                description="Desc",
                price=100,
                publisher=self.publisher,
                category=self.category,
                volume=10,
                number_of_pages=100,
                approximate_study_time=timedelta(days=5),
                publication_date=date(2025, 1, 1),
            )
            self.books.append(book)
            Favorite.objects.create(user=self.user, book=book)

        self.url = "/api/favorites/"

    def test_favorite_pagination_first_page(self):
        response = self.client.get(self.url + "?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 5)  # page_size از FavoritePagination
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["page_size"], 5)
        self.assertEqual(data["pages"], 3)
        self.assertEqual(data["count"], 12)
        self.assertIsNotNone(data["next"])
        self.assertIsNone(data["previous"])

    def test_favorite_pagination_second_page(self):
        response = self.client.get(self.url + "?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["page"], 2)
        self.assertEqual(data["previous"], f"http://testserver/api/favorites/?page=1")
        self.assertEqual(data["next"], f"http://testserver/api/favorites/?page=3")

    def test_favorite_pagination_last_page(self):
        response = self.client.get(self.url + "?page=3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(data["page"], 3)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], f"http://testserver/api/favorites/?page=2")

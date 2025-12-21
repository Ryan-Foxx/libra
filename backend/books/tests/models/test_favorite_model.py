from datetime import date, timedelta

from books.models import Author, Book, Category, Favorite, Publisher
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jack",
            email="user@test.com",
            password="password123",
        )

        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.category = Category.objects.create(title="Test Category")

        self.book = Book.objects.create(
            name="Test Book",
            description="Test Description",
            publisher=self.publisher,
            category=self.category,
            price=100,
            volume=10,
            number_of_pages=100,
            approximate_study_time=timedelta(days=10, hours=5, minutes=30, seconds=10),
            publication_date=date(2020, 5, 12),
        )
        self.book.authors.add(self.author)

    def test_create_favorite_successfully(self):
        favorite = Favorite.objects.create(user=self.user, book=self.book)

        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.book, self.book)

    def test_user_cannot_favorite_same_book_twice(self):
        Favorite.objects.create(user=self.user, book=self.book)

        with self.assertRaises(IntegrityError):
            Favorite.objects.create(user=self.user, book=self.book)

    def test_str_method_returns_user_book(self):
        favorite = Favorite.objects.create(user=self.user, book=self.book)
        self.assertEqual(str(favorite), f"{self.user} - {self.book}")

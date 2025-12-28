from datetime import date, timedelta

from books.models import (
    Author,
    Book,
    Category,
    ContentFormat,
    Language,
    Publisher,
    Rating,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class RatingModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456")

        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.category = Category.objects.create(title="Test Category")
        self.language = Language.objects.create(name="English")
        self.format = ContentFormat.objects.create(name="PDF")

        self.book = Book.objects.create(
            name="Test Book",
            description="Test Description",
            publisher=self.publisher,
            category=self.category,
            price=100,
            active=True,
            volume=10,
            number_of_pages=100,
            approximate_study_time=timedelta(hours=5),
            publication_date=date.today(),
        )

        self.book.authors.add(self.author)
        self.book.languages.add(self.language)
        self.book.content_formats.add(self.format)

    # @ Create a valid rating
    def test_create_valid_rating(self):
        rating = Rating.objects.create(user=self.user, book=self.book, score=4)

        self.assertEqual(rating.score, 4)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.book, self.book)

    # @ Score lower than minimum value (1)
    def test_rating_score_less_than_min_value(self):
        rating = Rating(user=self.user, book=self.book, score=0)

        with self.assertRaises(ValidationError):
            rating.full_clean()

    # @ Score greater than maximum value (5)
    def test_rating_score_greater_than_max_value(self):
        rating = Rating(user=self.user, book=self.book, score=6)

        with self.assertRaises(ValidationError):
            rating.full_clean()

    # @ A user cannot rate the same book more than once
    def test_user_cannot_rate_same_book_twice(self):
        Rating.objects.create(user=self.user, book=self.book, score=5)

        with self.assertRaises(IntegrityError):
            Rating.objects.create(user=self.user, book=self.book, score=3)

    # @ Test __str__ method
    def test_str_method_returns_name(self):
        rating = Rating.objects.create(user=self.user, book=self.book, score=5)

        expected_str = f"{self.user} rated {self.book} -> {rating.score}"
        self.assertEqual(str(rating), expected_str)

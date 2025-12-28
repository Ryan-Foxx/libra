from datetime import date, timedelta
from unittest.mock import Mock

from books.models import Book, Category, Publisher, Rating
from books.serializers.rating_serializers import RatingSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

User = get_user_model()


class TestRatingSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="jack",
            email="jack@test.com",
            password="password123",
            phone_number="0452384156",
        )

        cls.publisher = Publisher.objects.create(name="Publisher A")
        cls.category = Category.objects.create(title="Category A")

        cls.book = Book.objects.create(
            name="Book A",
            description="Desc",
            publisher=cls.publisher,
            category=cls.category,
            price=10000,
            active=True,
            volume=10,
            number_of_pages=100,
            approximate_study_time=timedelta(days=1),
            publication_date=date(2020, 5, 12),
        )

    def get_serializer(self, *, user, book_id, data):
        request = Mock()
        request.user = user

        view = Mock()
        view.action = "create"
        view.kwargs = {"book_pk": book_id}

        return RatingSerializer(
            data=data,
            context={
                "request": request,
                "view": view,
            },
        )

    def test_serializer_valid_data_passes(self):
        serializer = self.get_serializer(
            user=self.user,
            book_id=self.book.id,
            data={"score": 5},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_prevents_duplicate_rating(self):
        Rating.objects.create(
            user=self.user,
            book=self.book,
            score=4,
        )

        serializer = self.get_serializer(
            user=self.user,
            book_id=self.book.id,
            data={"score": 5},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("detail", serializer.errors)

    def test_user_and_book_are_read_only(self):
        serializer = self.get_serializer(
            user=self.user,
            book_id=self.book.id,
            data={
                "score": 4,
                "user": 999,
                "book": 999,
            },
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        validated_data = serializer.validated_data
        self.assertNotIn("user", validated_data)
        self.assertNotIn("book", validated_data)
        self.assertEqual(validated_data["score"], 4)

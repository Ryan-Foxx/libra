from datetime import date, timedelta

from books.models import Book, Category, Favorite, Publisher
from books.serializers.favorite_serializers import FavoriteSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestFavoriteSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jack",
            email="jack@test.com",
            password="password123",
            phone_number="+10000000001",
        )

        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.category = Category.objects.create(title="Test Category")

        self.book = Book.objects.create(
            name="Test Book",
            description="Some desc",
            publisher=self.publisher,
            category=self.category,
            price=100,
            active=False,
            volume=12,
            number_of_pages=220,
            approximate_study_time=timedelta(days=5),
            publication_date=date(2025, 1, 1),
        )

    def test_serializer_output_fields(self):
        favorite = Favorite.objects.create(user=self.user, book=self.book)
        serializer = FavoriteSerializer(favorite)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("book", data)
        self.assertIn("datetime_created", data)
        self.assertEqual(data["book"], self.book.id)

    def test_serializer_valid_data(self):
        data = {"book": self.book.id}
        serializer = FavoriteSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        instance = serializer.save(user=self.user)
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.book, self.book)

    def test_serializer_read_only_fields(self):
        data = {"book": self.book.id, "datetime_created": "2025-01-01T00:00:00Z"}
        serializer = FavoriteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save(user=self.user)

        self.assertNotEqual(instance.datetime_created.isoformat(), "2025-01-01T00:00:00+00:00")

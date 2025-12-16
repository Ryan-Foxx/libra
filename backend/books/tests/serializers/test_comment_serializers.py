from datetime import date, timedelta

from books.models import Book, Category, Comment, Publisher
from books.serializers.comment_serializers import CommentSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestCommentSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            email="user@test.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )

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
            publication_date=date(2023, 1, 1),
        )

    def test_comment_serializer_outputs_expected_fields(self):
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="Test comment",
        )

        data = CommentSerializer(comment).data

        self.assertIn("id", data)
        self.assertIn("user", data)
        self.assertIn("body", data)
        self.assertIn("datetime_created", data)

    def test_comment_serializer_user_is_nested(self):
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="Test comment",
        )

        data = CommentSerializer(comment).data

        self.assertIsInstance(data["user"], dict)
        self.assertEqual(data["user"]["username"], "john")
        self.assertEqual(data["user"]["first_name"], "John")
        self.assertEqual(data["user"]["last_name"], "Doe")

from datetime import date, timedelta

from books.models import Book, Category, Comment, Publisher
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class TestCommentViewSet(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", email="user@test.com", password="password123", first_name="John", last_name="Doe"
        )

        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.category = Category.objects.create(title="Test Category")

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

        self.client = APIClient()

    def test_authenticated_user_can_create_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-comments-list", kwargs={"book_pk": self.book.pk})
        response = self.client.post(url, data={"body": "Test comment"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        self.assertEqual(comment.body, "Test comment")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.book, self.book)

    def test_unauthenticated_user_cannot_create_comment(self):
        url = reverse("book-comments-list", kwargs={"book_pk": self.book.pk})
        response = self.client.post(url, data={"body": "Test comment"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 0)

    def test_list_only_returns_approved_comments(self):
        approved_comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="Approved comment",
            status=Comment.COMMENT_STATUS_APPROVED,
        )

        url = reverse("book-comments-list", kwargs={"book_pk": self.book.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["body"], approved_comment.body)

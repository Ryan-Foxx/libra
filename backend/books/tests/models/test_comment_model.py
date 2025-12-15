from datetime import date, timedelta

from books.models import Book, Category, Comment, Publisher
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestCommentModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jack",
            email="user@test.com",
            password="password123",
        )

        self.publisher = Publisher.objects.create(name="Publisher A")
        self.category = Category.objects.create(title="Category A")

        self.book = Book.objects.create(
            name="Book A",
            description="Desc",
            publisher=self.publisher,
            category=self.category,
            price=10000,
            active=True,
            volume=10,
            number_of_pages=100,
            approximate_study_time=timedelta(days=10, hours=5, minutes=30, seconds=10),
            publication_date=date(2020, 5, 12),
        )

    def test_comment_is_created_successfully(self):
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="This is a test comment",
        )

        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.book, self.book)
        self.assertEqual(comment.body, "This is a test comment")

    def test_comment_default_status_is_waiting(self):
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="Waiting comment",
        )

        self.assertEqual(
            comment.status,
            Comment.COMMENT_STATUS_WAITING,
        )

    def test_comment_status_can_be_changed_to_approved(self):
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="Approved comment",
            status=Comment.COMMENT_STATUS_APPROVED,
        )

        self.assertEqual(
            comment.status,
            Comment.COMMENT_STATUS_APPROVED,
        )

    def test_comment_is_deleted_when_user_is_deleted(self):
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="Cascade user delete",
        )

        self.user.delete()

        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_comment_is_deleted_when_book_is_deleted(self):
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            body="Cascade book delete",
        )

        self.book.delete()

        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

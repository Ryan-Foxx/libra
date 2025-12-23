from datetime import date, timedelta

from books.models import (
    Author,
    Book,
    Category,
    ContentFormat,
    Favorite,
    Language,
    Publisher,
    Translator,
)
from books.serializers.book_serializers import BookSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory

User = get_user_model()


class TestBookSerializer(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.author = Author.objects.create(name="Author A")
        self.translator = Translator.objects.create(name="Translator A")
        self.publisher = Publisher.objects.create(name="Publisher A")
        self.category = Category.objects.create(title="Category A")
        self.language = Language.objects.create(name="Lang A")
        self.content_format = ContentFormat.objects.create(name="Format A")

        self.book = Book.objects.create(
            name="Book A",
            description="Some desc",
            publisher=self.publisher,
            category=self.category,
            price=100,
            active=False,
            volume=12,
            number_of_pages=220,
            approximate_study_time=timedelta(days=10, hours=5, minutes=30, seconds=10),
            publication_date=date(2024, 1, 1),
        )

        self.book.authors.add(self.author)
        self.book.translators.add(self.translator)
        self.book.languages.add(self.language)
        self.book.content_formats.add(self.content_format)

    def test_book_serializer_outputs_expected_fields_for_anonymous_user(self):
        request = self.factory.get("/fake-url/")
        request.user = AnonymousUser()

        data = BookSerializer(self.book, context={"request": request}).data

        self.assertEqual(data["name"], "Book A")
        self.assertEqual(data["publisher"]["name"], "Publisher A")
        self.assertEqual(len(data["authors"]), 1)
        self.assertEqual(len(data["languages"]), 1)

        # is_favorited
        self.assertIn("is_favorited", data)
        self.assertFalse(data["is_favorited"])

    def test_book_serializer_is_favorited_true_for_user_with_favorite(self):
        user = User.objects.create_user(
            username="jack",
            password="password123",
            phone_number="+10000000001",
        )

        Favorite.objects.create(user=user, book=self.book)

        request = self.factory.get("/fake-url/")
        request.user = user

        context = {
            "request": request,
            "favorite_book_ids": {self.book.id},
        }

        data = BookSerializer(self.book, context=context).data
        self.assertTrue(data["is_favorited"])

    def test_book_serializer_is_favorited_false_for_user_without_favorite(self):
        user = User.objects.create_user(
            username="jane",
            password="password123",
            phone_number="+10000000002",
        )

        request = self.factory.get("/fake-url/")
        request.user = user

        data = BookSerializer(self.book, context={"request": request}).data
        self.assertFalse(data["is_favorited"])

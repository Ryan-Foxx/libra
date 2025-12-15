from datetime import date, timedelta

from books.models import (
    Author,
    Book,
    Category,
    ContentFormat,
    Language,
    Publisher,
    Translator,
)
from books.serializers.book_serializers import BookSerializer
from django.test import TestCase


class TestBookSerializer(TestCase):
    def test_book_serializer_outputs_expected_fields(self):
        author = Author.objects.create(name="Author A")
        translator = Translator.objects.create(name="Translator A")
        publisher = Publisher.objects.create(name="Publisher A")
        category = Category.objects.create(title="Category A")
        language = Language.objects.create(name="Lang A")
        content_format = ContentFormat.objects.create(name="Format A")

        book = Book.objects.create(
            name="Book A",
            description="Some desc",
            publisher=publisher,
            category=category,
            price=100,
            active=False,
            volume=12,
            number_of_pages=220,
            approximate_study_time=timedelta(days=10, hours=5, minutes=30, seconds=10),
            publication_date=date(2024, 1, 1),
        )

        book.authors.add(author)
        book.translators.add(translator)
        book.languages.add(language)
        book.content_formats.add(content_format)

        data = BookSerializer(book).data

        self.assertEqual(data["name"], "Book A")
        self.assertEqual(data["publisher"]["name"], "Publisher A")
        self.assertEqual(len(data["authors"]), 1)
        self.assertEqual(len(data["languages"]), 1)

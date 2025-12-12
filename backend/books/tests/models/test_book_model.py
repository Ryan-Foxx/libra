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
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class TestBookModel(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name="Author A")
        self.translator = Translator.objects.create(name="Translator A")
        self.publisher = Publisher.objects.create(name="Pub A")
        self.category = Category.objects.create(title="Cat A")
        self.format_pdf = ContentFormat.objects.create(name="PDF")
        self.lang_en = Language.objects.create(name="English")

    # -----------------
    # @ Creation Tests
    # -----------------

    def test_create_book_successfully(self):
        book = Book.objects.create(
            name="Book A",
            description="Some description",
            publisher=self.publisher,
            category=self.category,
            price=10000,
            active=True,
            volume=10,
            number_of_pages=150,
            approximate_study_time=timedelta(days=10, hours=5, minutes=30, seconds=10),
            publication_date=date(2020, 5, 12),
        )

        # @ Add ManyToManyField
        book.authors.add(self.author)
        book.translators.add(self.translator)
        book.content_formats.add(self.format_pdf)
        book.languages.add(self.lang_en)

        self.assertEqual(book.name, "Book A")
        self.assertEqual(book.description, "Some description")
        self.assertEqual(book.publisher, self.publisher)
        self.assertEqual(book.category, self.category)
        self.assertEqual(book.price, 10000)
        self.assertIn(book.active, [True, False])
        self.assertEqual(book.volume, 10)
        self.assertEqual(book.number_of_pages, 150)
        self.assertEqual(book.approximate_study_time, timedelta(days=10, hours=5, minutes=30, seconds=10))
        self.assertEqual(book.publication_date, date(2020, 5, 12))
        self.assertIsNotNone(book.datetime_created)
        self.assertIsNotNone(book.datetime_modified)
        self.assertIn(self.author, book.authors.all())
        self.assertIn(self.translator, book.translators.all())
        self.assertIn(self.format_pdf, book.content_formats.all())
        self.assertIn(self.lang_en, book.languages.all())

    # ----------------------------------------
    # @ Unique & Max Length Field Validations
    # ----------------------------------------

    def test_name_max_length_validation(self):
        long_name = "a" * 256
        book = Book(name=long_name)

        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_name_must_be_unique(self):
        Book.objects.create(
            name="Unique Book",
            description="Some description",
            publisher=self.publisher,
            category=self.category,
            volume=1,
            number_of_pages=1,
            approximate_study_time=timedelta(hours=1),
            publication_date=date.today(),
        )

        with self.assertRaises(IntegrityError):
            Book.objects.create(
                name="Unique Book",
                description="Some description",
                publisher=self.publisher,
                category=self.category,
                volume=1,
                number_of_pages=1,
                approximate_study_time=timedelta(hours=1),
                publication_date=date.today(),
            )

    # -------------------------
    # @ Positive Number Fields
    # -------------------------

    def test_volume_must_be_positive(self):
        book = Book(
            name="Bad Book",
            description="desc",
            publisher=self.publisher,
            category=self.category,
            volume=-1,
            number_of_pages=10,
            approximate_study_time=timedelta(hours=1),
            publication_date=date.today(),
        )

        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_number_of_pages_must_be_positive(self):
        book = Book(
            name="Bad Book 2",
            description="desc",
            publisher=self.publisher,
            category=self.category,
            volume=10,
            number_of_pages=-5,
            approximate_study_time=timedelta(hours=1),
            publication_date=date.today(),
        )

        with self.assertRaises(ValidationError):
            book.full_clean()

    # ----------------------------------------------
    # @ ForeignKey (on_delete=models.PROTECT) Tests
    # ----------------------------------------------

    def test_publisher_on_delete_protect(self):
        book = Book.objects.create(
            name="BookX",
            description="desc",
            publisher=self.publisher,
            category=self.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time=timedelta(hours=1),
            publication_date=date.today(),
        )

        with self.assertRaises(IntegrityError):
            self.publisher.delete()

    def test_category_on_delete_protect(self):
        Book.objects.create(
            name="BookY",
            description="desc",
            publisher=self.publisher,
            category=self.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time=timedelta(hours=1),
            publication_date=date.today(),
        )

        with self.assertRaises(IntegrityError):
            self.category.delete()

    # ---------------------------
    # @ Default & Boolean Fields
    # ---------------------------

    def test_price_default_zero(self):
        book = Book.objects.create(
            name="Free Book",
            description="desc",
            publisher=self.publisher,
            category=self.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time=timedelta(hours=1),
            publication_date=date.today(),
        )

        self.assertEqual(book.price, 0)

    def test_active_default_false(self):
        book = Book.objects.create(
            name="Inactive Book",
            description="desc",
            publisher=self.publisher,
            category=self.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time=timedelta(hours=1),
            publication_date=date.today(),
        )

        self.assertFalse(book.active)

    # -------------------------
    # @ String Representation
    # -------------------------

    def test_str_returns_name(self):
        book = Book.objects.create(
            name="Nice Book",
            description="desc",
            publisher=self.publisher,
            category=self.category,
            volume=1,
            number_of_pages=10,
            approximate_study_time=timedelta(hours=2),
            publication_date=date.today(),
        )

        self.assertEqual(str(book), "Nice Book")

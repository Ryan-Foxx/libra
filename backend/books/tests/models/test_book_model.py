import os
import tempfile
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
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings


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


# --------------------
# @ Cover Image Tests
# --------------------
TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestBookCoverImageModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher = Publisher.objects.create(name="Pub A")
        cls.category = Category.objects.create(title="Cat A")

    def get_test_image(self, name="cover.jpg"):
        return SimpleUploadedFile(
            name=name,
            content=b"\x47\x49\x46\x38\x39\x61",
            content_type="image/jpeg",
        )

    def _create_book(self, **kwargs):
        data = {
            "name": "Test Book",
            "description": "desc",
            "publisher": self.publisher,
            "category": self.category,
            "volume": 1,
            "number_of_pages": 10,
            "approximate_study_time": "01:00:00",
            "publication_date": date.today(),
        }
        data.update(kwargs)
        return Book.objects.create(**data)

    def test_cover_image_is_renamed_after_save(self):

        book = self._create_book(cover_image=self.get_test_image("my_cover.jpg"))

        self.assertTrue(book.cover_image)
        self.assertTrue(book.cover_image.name.startswith("books/covers/"))
        self.assertTrue(book.cover_image.name.endswith(".jpg"))
        self.assertIn(str(book.id), book.cover_image.name)

        self.assertTrue(os.path.exists(book.cover_image.path))

    def test_replacing_cover_image_replaces_file_not_duplicates(self):

        book = self._create_book(cover_image=self.get_test_image("old.jpg"))

        first_path = book.cover_image.path
        self.assertTrue(os.path.exists(first_path))

        book.cover_image = self.get_test_image("new.jpg")
        book.save()

        book.refresh_from_db()
        second_path = book.cover_image.path

        self.assertEqual(first_path, second_path)

        self.assertTrue(os.path.exists(second_path))

        covers_dir = os.path.dirname(second_path)
        temp_files = [f for f in os.listdir(covers_dir) if f.startswith("temp_")]
        self.assertEqual(
            temp_files,
            [],
            "Temporary cover files should not remain after replace",
        )

    def test_clearing_cover_image_deletes_file_from_disk(self):

        book = self._create_book(cover_image=self.get_test_image("clear.jpg"))

        file_path = book.cover_image.path
        self.assertTrue(os.path.exists(file_path))

        # simulate admin clear
        book.cover_image = None
        book.save()

        self.assertFalse(book.cover_image)
        self.assertFalse(
            os.path.exists(file_path),
            "Cover image file should be deleted after clearing field",
        )

    def test_deleting_book_deletes_cover_image_file(self):

        book = self._create_book(cover_image=self.get_test_image("delete.jpg"))

        file_path = book.cover_image.path
        self.assertTrue(os.path.exists(file_path))

        book.delete()

        self.assertFalse(
            os.path.exists(file_path),
            "Cover image file should be deleted after book deletion",
        )

    def test_cover_image_field_definition(self):

        field = Book._meta.get_field("cover_image")

        self.assertTrue(field.null)
        self.assertTrue(field.blank)

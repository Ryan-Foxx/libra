from books.models import Category
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class TestCategoryModel(TestCase):

    def test_create_category_successfully(self):
        category = Category.objects.create(title="Fiction", description="All fictional works.")

        self.assertEqual(category.title, "Fiction")
        self.assertEqual(category.description, "All fictional works.")

    def test_title_max_length_validation(self):
        long_title = "a" * 51
        category = Category(title=long_title)

        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_title_must_be_unique(self):
        Category.objects.create(title="History")

        with self.assertRaises(IntegrityError):
            Category.objects.create(title="History")

    def test_description_max_length_validation(self):
        long_desc = "a" * 501
        category = Category(title="Poetry", description=long_desc)

        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_description_can_be_blank(self):
        category = Category.objects.create(title="Science", description="")
        self.assertEqual(category.description, "")

    def test_str_method_returns_title(self):
        category = Category.objects.create(title="Str Test")
        self.assertEqual(str(category), "Str Test")

from books.models import (
    Author,
    Book,
    Category,
    ContentFormat,
    Language,
    Publisher,
    Translator,
)
from books.serializers.book_image_serializers import BookImageSerializer
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "biography", "datetime_created"]


class TranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translator
        fields = ["id", "name", "about", "datetime_created"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "about", "datetime_created"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "description"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]


class ContentFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentFormat
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):

    images = BookImageSerializer(many=True, read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)
    translators = TranslatorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    content_formats = ContentFormatSerializer(many=True, read_only=True)

    # @ Custom Method Field
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "name",
            "description",
            "cover_image",
            "images",
            "authors",
            "translators",
            "publisher",
            "category",
            "languages",
            "content_formats",
            "price",
            "active",
            "volume",
            "number_of_pages",
            "approximate_study_time",
            "publication_date",
            "datetime_created",
            "datetime_modified",
            "is_favorited",
        ]

    def get_is_favorited(self, book: Book):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        favorite_book_ids = self.context.get("favorite_book_ids", set())
        return book.id in favorite_book_ids

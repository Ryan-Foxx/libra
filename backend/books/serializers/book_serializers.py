from books.models import (
    Author,
    Book,
    Category,
    ContentFormat,
    Language,
    Publisher,
    Translator,
)
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

    authors = AuthorSerializer(many=True, read_only=True)
    translators = TranslatorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    content_formats = ContentFormatSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "name",
            "description",
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
        ]

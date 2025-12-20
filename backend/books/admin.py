from django.contrib import admin

from .models import (
    Author,
    Book,
    BookImage,
    Category,
    Comment,
    ContentFormat,
    Language,
    Publisher,
    Translator,
)


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "biography", "datetime_created"]
    list_per_page = 10


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "about", "datetime_created"]
    list_per_page = 10


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "about", "datetime_created"]
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description"]
    list_per_page = 10


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_per_page = 10


@admin.register(ContentFormat)
class ContentFormatAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_per_page = 10


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        # "description",
        # "authors",
        # "translators",
        "publisher",
        "category",
        "price",
        "active",
        # "content_formats",
        # "languages",
        "volume",
        "number_of_pages",
        "approximate_study_time",
        "publication_date",
        "datetime_created",
        "datetime_modified",
    ]
    list_per_page = 10


@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ["id", "book", "image", "description"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "book", "body", "datetime_created", "status"]
    list_per_page = 10

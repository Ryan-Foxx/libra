from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils.paths import book_cover_upload_path, book_image_upload_path


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    biography = models.TextField(blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Translator(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True)
    about = models.TextField(blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)
    about = models.TextField(blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ContentFormat(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to=book_cover_upload_path, null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name="books")
    translators = models.ManyToManyField(Translator, related_name="books", blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="books")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    price = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    active = models.BooleanField(default=False)
    content_formats = models.ManyToManyField(ContentFormat, related_name="books")
    languages = models.ManyToManyField(Language, related_name="books")
    volume = models.PositiveIntegerField(help_text="Book size in MB")
    number_of_pages = models.PositiveIntegerField()
    approximate_study_time = models.DurationField()
    publication_date = models.DateField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=book_image_upload_path, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Image for {self.book.name}"


class Comment(models.Model):
    COMMENT_STATUS_WAITING = "w"
    COMMENT_STATUS_APPROVED = "a"
    COMMENT_STATUS_NOT_APPROVED = "na"
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, "Waiting"),
        (COMMENT_STATUS_APPROVED, "Approved"),
        (COMMENT_STATUS_NOT_APPROVED, "Not Approved"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorites")
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "book"], name="unique_books_favorite_user_book")]

    def __str__(self):
        return f"{self.user} - {self.book}"


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "book"], name="unique_books_rating_user_book")]

    def __str__(self):
        return f"{self.user} rated {self.book} -> {self.score}"

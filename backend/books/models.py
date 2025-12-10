from django.db import models


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

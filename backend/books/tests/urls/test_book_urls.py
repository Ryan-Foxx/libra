from books.views import BookViewSet
from django.test import SimpleTestCase
from django.urls import resolve, reverse


class TestBookUrls(SimpleTestCase):
    def test_books_list_url_resolves(self):
        url = reverse("book-list")
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, BookViewSet, "The 'book-list' URL should resolve to BookViewSet")

    def test_books_detail_url_resolves(self):
        url = reverse("book-detail", args=[1])
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, BookViewSet, "The 'book-detail' URL should resolve to BookViewSet")

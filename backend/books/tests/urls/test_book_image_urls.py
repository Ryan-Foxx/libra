from books.views import BookImageViewSet
from django.urls import resolve, reverse
from rest_framework.routers import DefaultRouter
from rest_framework.test import APITestCase


class TestBookImageUrls(APITestCase):

    def test_book_images_list_url_resolves(self):
        url = reverse("book-images-list", kwargs={"book_pk": 1})
        resolver = resolve(url)

        self.assertEqual(resolver.func.cls, BookImageViewSet)

    def test_book_images_detail_url_resolves(self):
        url = reverse(
            "book-images-detail",
            kwargs={"book_pk": 1, "pk": 1},
        )
        resolver = resolve(url)

        self.assertEqual(resolver.func.cls, BookImageViewSet)

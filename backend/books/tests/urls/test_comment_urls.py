from books.views import CommentViewSet
from django.test import SimpleTestCase
from django.urls import resolve, reverse


class TestCommentUrls(SimpleTestCase):
    def test_book_comments_list_url_resolves(self):
        url = reverse("book-comments-list", args=[1])
        resolver = resolve(url)

        self.assertEqual(resolver.func.cls, CommentViewSet)

    def test_book_comments_detail_url_resolves(self):
        url = reverse("book-comments-detail", args=[1, 1])
        resolver = resolve(url)

        self.assertEqual(resolver.func.cls, CommentViewSet)

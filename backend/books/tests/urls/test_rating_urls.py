from datetime import date, timedelta

from books.models import Book, Category, Publisher, Rating
from books.views import RatingViewSet
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestRatingUrls(APITestCase):
    """
    Rating feature tests:
    - url resolving
    - authentication
    - list behavior
    - create behavior
    - validation
    """

    @classmethod
    def setUpTestData(cls):
        # @ users
        cls.user1 = User.objects.create_user(
            username="jack",
            email="jack@test.com",
            password="password123",
            phone_number="0452384156",
        )
        cls.user2 = User.objects.create_user(
            username="sarah",
            email="sarah@test.com",
            password="password123",
            phone_number="0452484156",
        )

        # @ book requirements
        cls.publisher = Publisher.objects.create(name="Publisher A")
        cls.category = Category.objects.create(title="Category A")

        cls.book = Book.objects.create(
            name="Book A",
            description="Desc",
            publisher=cls.publisher,
            category=cls.category,
            price=10000,
            active=True,
            volume=10,
            number_of_pages=100,
            approximate_study_time=timedelta(days=1),
            publication_date=date(2020, 5, 12),
        )

    # @ ---------- helpers ----------
    def ratings_list_url(self):
        return reverse("book-ratings-list", args=[self.book.id])

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # @ ---------- URL resolving ----------
    def test_book_ratings_list_url_resolves(self):
        url = reverse("book-ratings-list", args=[1])
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, RatingViewSet)

    def test_book_ratings_detail_url_resolves(self):
        url = reverse("book-ratings-detail", args=[1, 1])
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, RatingViewSet)

    # @ ---------- authentication ----------
    def test_anonymous_user_cannot_access_ratings_list(self):
        response = self.client.get(self.ratings_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # @ ---------- list ----------
    def test_user_sees_only_own_rating(self):
        Rating.objects.create(user=self.user1, book=self.book, score=4)
        Rating.objects.create(user=self.user2, book=self.book, score=5)

        self.authenticate(self.user1)
        response = self.client.get(self.ratings_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["score"], 4)

    # @ ---------- create ----------
    def test_authenticated_user_can_create_rating(self):
        self.authenticate(self.user1)

        response = self.client.post(self.ratings_list_url(), {"score": 5})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)

        rating = Rating.objects.first()
        self.assertEqual(rating.user, self.user1)
        self.assertEqual(rating.book, self.book)
        self.assertEqual(rating.score, 5)

    def test_user_cannot_create_duplicate_rating(self):
        Rating.objects.create(user=self.user1, book=self.book, score=4)
        self.authenticate(self.user1)

        response = self.client.post(self.ratings_list_url(), {"score": 5})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rating.objects.count(), 1)

    #  @---------- validation ----------
    def test_score_lower_than_1_returns_400(self):
        self.authenticate(self.user1)

        response = self.client.post(self.ratings_list_url(), {"score": 0})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rating.objects.count(), 0)

    def test_score_greater_than_5_returns_400(self):
        self.authenticate(self.user1)

        response = self.client.post(self.ratings_list_url(), {"score": 6})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rating.objects.count(), 0)

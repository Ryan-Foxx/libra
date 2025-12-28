from datetime import date, timedelta

from books.models import Book, Category, Publisher, Rating
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestRatingViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="jack",
            email="jack@test.com",
            password="password123",
            phone_number="0452384156",
        )
        cls.other_user = User.objects.create_user(
            username="sarah",
            email="sarah@test.com",
            password="password123",
            phone_number="0452484156",
        )

        cls.publisher = Publisher.objects.create(name="Publisher A")
        cls.category = Category.objects.create(title="Category A")

        cls.book1 = Book.objects.create(
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

        cls.book2 = Book.objects.create(
            name="Book B",
            description="Desc",
            publisher=cls.publisher,
            category=cls.category,
            price=12000,
            active=True,
            volume=5,
            number_of_pages=200,
            approximate_study_time=timedelta(days=2),
            publication_date=date(2021, 1, 1),
        )

    # @ -------- helpers --------
    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def ratings_url(self, book):
        return reverse("book-ratings-list", args=[book.id])

    # @ -------- get_queryset --------
    def test_get_queryset_returns_only_current_user_ratings_for_book(self):
        Rating.objects.create(user=self.user, book=self.book1, score=4)
        Rating.objects.create(user=self.other_user, book=self.book1, score=5)
        Rating.objects.create(user=self.user, book=self.book2, score=3)

        self.authenticate()
        response = self.client.get(self.ratings_url(self.book1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["score"], 4)

    # @ -------- perform_create --------
    def test_perform_create_sets_user_and_book_automatically(self):
        self.authenticate()

        response = self.client.post(self.ratings_url(self.book1), {"score": 5})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating = Rating.objects.first()
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.book, self.book1)

    def test_client_cannot_override_user_or_book(self):
        self.authenticate()

        response = self.client.post(
            self.ratings_url(self.book1),
            {
                "score": 4,
                "user": self.other_user.id,
                "book": self.book2.id,
            },
        )

        # @ API contract
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # @ business rule
        rating = Rating.objects.first()
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.book, self.book1)

    # @ -------- allowed methods --------
    def test_put_method_not_allowed(self):
        self.authenticate()

        response = self.client.put(self.ratings_url(self.book1), {"score": 3})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_not_allowed(self):
        self.authenticate()

        response = self.client.delete(self.ratings_url(self.book1))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

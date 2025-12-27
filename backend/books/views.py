from books.filters.book_filters import BookFilter
from books.serializers.book_image_serializers import BookImageSerializer
from books.serializers.favorite_serializers import FavoriteSerializer
from books.serializers.rating_serializers import RatingSerializer
from core.pagination.books import BookPagination
from core.pagination.favorites import FavoritePagination
from django.db.models import Avg, Count, IntegerField, OuterRef, Subquery, Value
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Book, BookImage, Comment, Favorite, Rating
from .serializers.book_serializers import BookSerializer
from .serializers.comment_serializers import CommentSerializer


# Create your views here.
class BookViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ["price", "datetime_created", "datetime_modified"]
    pagination_class = BookPagination

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Book.objects.select_related("publisher", "category")
            .prefetch_related("images", "authors", "translators", "content_formats", "languages")
            .annotate(
                avg_rating=Avg("ratings__score"),
                rating_count=Count("ratings__id"),
            )
            .order_by("-datetime_created")
            .distinct()
            .all()
        )

        if user.is_authenticated:
            queryset = queryset.annotate(
                my_rating=Subquery(
                    Rating.objects.filter(
                        book=OuterRef("pk"),
                        user=user,
                    ).values("score"),
                    output_field=IntegerField(),
                )
            )
        else:
            queryset = queryset.annotate(my_rating=Value(None, output_field=IntegerField()))

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user

        if user.is_authenticated:
            favorite_book_ids = set(Favorite.objects.filter(user=user).values_list("book_id", flat=True))
        else:
            favorite_book_ids = set()

        context["favorite_book_ids"] = favorite_book_ids
        return context


class BookImageViewSet(ReadOnlyModelViewSet):
    serializer_class = BookImageSerializer

    def get_queryset(self):
        book_pk = self.kwargs["book_pk"]
        return BookImage.objects.filter(book__id=book_pk).all()


class CommentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        book_pk = self.kwargs["book_pk"]
        return (
            Comment.objects.select_related("user")
            .filter(book__id=book_pk, status=Comment.COMMENT_STATUS_APPROVED)
            .order_by("-datetime_created")
            .all()
        )

    def perform_create(self, serializer):
        book_pk = self.kwargs["book_pk"]
        serializer.save(user=self.request.user, book_id=book_pk)


class FavoriteViewSet(ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    serializer_class = FavoriteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = FavoritePagination

    def get_queryset(self):
        user_id = self.request.user.id
        return Favorite.objects.filter(user__id=user_id).order_by("-datetime_created").all()

    def create(self, request):
        book_id = request.data.get("book")
        favorite = Favorite.objects.filter(user=request.user, book_id=book_id).first()

        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RatingViewSet(ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @ Return only current user's rating for the selected book
    def get_queryset(self):
        book_pk = self.kwargs["book_pk"]
        return Rating.objects.select_related("user").filter(user=self.request.user, book_id=book_pk)

    # @ Create rating
    def perform_create(self, serializer):
        book_pk = self.kwargs["book_pk"]
        serializer.save(user=self.request.user, book_id=book_pk)

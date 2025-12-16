from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Book, Comment
from .serializers.book_serializers import BookSerializer
from .serializers.comment_serializers import CommentSerializer


# Create your views here.
class BookViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer

    queryset = (
        Book.objects.select_related("publisher", "category")
        .prefetch_related("authors", "translators", "content_formats", "languages")
        .order_by("-datetime_created")
        .all()
    )


class CommentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication]

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

from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers.book_serializers import BookSerializer

from .models import Book


# Create your views here.
class BookViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer

    queryset = (
        Book.objects.select_related("publisher", "category")
        .prefetch_related("authors", "translators", "content_formats", "languages")
        .order_by("-datetime_created")
        .all()
    )

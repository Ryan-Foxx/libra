from books.models import Book
from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet


class BookFilter(FilterSet):
    # @ ------------ search (free text) ------------
    search = CharFilter(method="global_search")

    # @ ------------ simple filters ------------
    category = CharFilter(field_name="category__title", lookup_expr="icontains")

    # @ ------------ relational filters ------------
    author = CharFilter(method="filter_search")
    translator = CharFilter(method="filter_search")
    publisher = CharFilter(method="filter_search")
    language = CharFilter(method="filter_search")
    formats = CharFilter(method="filter_search")

    class Meta:
        model = Book
        fields = []

    # @ -------- search implementation --------
    def global_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(authors__name__icontains=value)
            | Q(translators__name__icontains=value)
            | Q(publisher__name__icontains=value)
        )

    def filter_search(self, queryset, name, value):
        filters_map = {
            "author": Q(authors__name__icontains=value),
            "translator": Q(translators__name__icontains=value),
            "publisher": Q(publisher__name__icontains=value),
            "language": Q(languages__name__icontains=value),
            "formats": Q(content_formats__name__icontains=value),
        }

        q_object = filters_map.get(name)
        if not q_object:
            return queryset

        return queryset.filter(q_object)

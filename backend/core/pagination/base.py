from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        previous_link = None

        if self.page.has_previous():
            prev_page = self.page.previous_page_number()
            request = self.request
            base_url = request.build_absolute_uri(request.path)

            if prev_page == 1:
                previous_link = f"{base_url}?page=1"
            else:
                previous_link = f"{base_url}?page={prev_page}"

        return Response(
            {
                "count": self.page.paginator.count,
                "pages": self.page.paginator.num_pages,
                "page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "next": self.get_next_link(),
                "previous": previous_link,
                "results": data,
            }
        )

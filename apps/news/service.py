from rest_framework.pagination import PageNumberPagination

from .models import News


class PaginationNews(PageNumberPagination):
    page_size = 2
    max_page_size = 1000


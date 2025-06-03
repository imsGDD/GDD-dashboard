from rest_framework.pagination import PageNumberPagination

class ActionAllPagination(PageNumberPagination):
    page_size = 10
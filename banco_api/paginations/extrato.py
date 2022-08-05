import re

from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class ExtratoPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"

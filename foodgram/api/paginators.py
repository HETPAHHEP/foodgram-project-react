from rest_framework.pagination import PageNumberPagination


class CustomPaginationRecipe(PageNumberPagination):
    """Своя пагинация страниц рецептов"""
    page_size_query_param = 'limit'

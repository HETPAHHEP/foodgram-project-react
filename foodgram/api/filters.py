from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов"""
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.CharFilter(
        field_name='tags__slug',
        method='filter_tags',
        lookup_expr='in'
    )

    class Meta:
        model = Recipe
        fields = ['author']

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            favorited_recipes = user.favorites.values_list('recipe', flat=True)
            queryset = queryset.filter(pk__in=favorited_recipes)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            recipes_in_cart = user.cart.values_list('recipe', flat=True)
            queryset = queryset.filter(pk__in=recipes_in_cart)
        return queryset

    def filter_tags(self, queryset, name, value):
        tags = self.request.GET.getlist('tags')
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()

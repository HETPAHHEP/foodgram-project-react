from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Отображения всех тегов"""
    list_display = ['id', 'name', 'slug', 'color', 'colored_hex']

    def colored_hex(self, obj):
        """Демонстрация цвета в панели"""
        return format_html(
            f'<span style="color: {obj.color};">{obj.color}</span>'
        )

    colored_hex.short_description = _('Показ цвета')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Отображения всех ингредиентов"""
    list_display = ['id', 'name', 'measurement_unit']
    list_filter = ['name']
    search_fields = ['name']


class IngredientsInline(admin.TabularInline):
    """Отображения ингредиентов рецепта"""
    model = RecipeIngredient
    min_num = 1
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Отображения рецептов пользователей"""
    list_display = [
        'id', 'name', 'author',
        'display_image', 'get_favorites'
    ]
    fields = [
        'name', 'author', 'cooking_time',
        'tags', 'image', 'text', 'get_favorites'
    ]
    inlines = [IngredientsInline]
    list_filter = ['name', 'author', 'tags']
    readonly_fields = ['get_favorites']
    search_fields = ['name']

    def get_favorites(self, obj):
        """Счетчик добавлено в избранное у рецепта"""
        return obj.in_favorite.count()

    def display_image(self, obj):
        """Отображение фото рецепта"""
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" width="100" height="100" />'
            )

    display_image.short_description = _('Фото')
    get_favorites.short_description = _('В избранном')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Отображения избранных рецептов пользователей"""
    list_display = ['user', 'recipe']
    search_fields = ['user', 'recipe']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Отображения корзины рецептов пользователей"""
    list_display = ['user', 'recipe']
    search_fields = ['user', 'recipe']

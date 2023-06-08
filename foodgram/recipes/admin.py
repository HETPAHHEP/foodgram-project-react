from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Ingredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'color', 'colored_hex']

    def colored_hex(self, obj):
        """Демонстрация цвета в панели"""
        return format_html(
            f'<span style="color: {obj.color};">{obj.color}</span>'
        )

    colored_hex.short_description = _('Показ цвета')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    list_filter = ['name']
    search_fields = ['name']

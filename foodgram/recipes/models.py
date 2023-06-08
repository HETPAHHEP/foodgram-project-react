from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import HexColorValidator


class Recipe(models.Model):
    """Модель рецептов"""
    pass


class Ingredient(models.Model):
    """Модель ингредиентов для рецептов"""
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название ингредиента')
    )
    measurement_unit = models.CharField(
        max_length=80,
        verbose_name=_('Единица измерения')
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        unique_together = ['name', 'measurement_unit']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов для рецептов"""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Имя тега')
    )
    color = models.CharField(
        max_length=7,
        validators=[HexColorValidator()],
        default='#FFFFFF',
        verbose_name=_('Цвет')
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.slug

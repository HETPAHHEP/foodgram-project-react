from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import HexColorValidator

CustomUser = get_user_model()


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
        default='#FFFFFF',  # Белый цвет
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
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название рецепта')
    )
    text = models.TextField(
        max_length=2000,
        verbose_name=_('Описание рецепта')
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message=_(
                'Добавьте необходимое время приготовления '
                '(минимальное значение: 1 минута).')),
            MaxValueValidator(300, message=_(
                'Максимально возможное время приготовления достигнуто '
                '(максимальное значение: 300 минут).'))
        ],
        verbose_name=_('Время приготовления')
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name=_('Изображение рецепта')
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name=_('Автор')
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name=_('Ингредиенты')
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name=_('Теги'),
    )
    pub_date = models.DateTimeField(
        editable=False,
        auto_now_add=True,
        verbose_name=_('Дата публикации')
    )

    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe_name_per_author'
            )
        ]


class RecipeIngredient(models.Model):
    """Сводная таблица отношения ManyToMany для рецептов и ингредиентов"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name=_('Рецепт')
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name=_('Ингредиент')
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('Количество'),
        validators=[
            MinValueValidator(
                1,
                message=_('Добавьте нужное количество ингредиента')
            ),  # Минимальное количество ингредиента: 1 ед.
            MaxValueValidator(
                10_000,
                message=_('Убавьте количество ингредиента')
            )  # Максимальное количество ингредиента: 10 000 ед.
        ],
    )

    class Meta:
        verbose_name = _('Количество ингредиента')
        verbose_name_plural = _('Количество у ингредиентов')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} — {self.amount}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name=_('Избранные рецепты')
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('Пользователь')
    )
    date_add = models.DateTimeField(
        editable=False,
        auto_now_add=True,
        verbose_name=_('Дата добавления')
    )

    class Meta:
        verbose_name = _('Избранный рецепт')
        verbose_name_plural = _('Избранные рецепты')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} — {self.recipe}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_cart',
        verbose_name=_('Рецепты в корзине')
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('Пользователь')
    )
    date_add = models.DateTimeField(
        editable=False,
        auto_now_add=True,
        verbose_name=_('Дата добавления')
    )

    class Meta:
        verbose_name = _('Рецепт в корзине')
        verbose_name_plural = _('Рецепты в корзине')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shopping_cart_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} — {self.recipe}'

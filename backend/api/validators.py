from django.utils.translation import gettext_lazy as _

from .exceptions import (FavoriteExistsError, IngredientDuplicateError,
                         IngredientLimitError, ShoppingCartExistsError,
                         SubscriptionExistsError, SubscriptionYouError,
                         TagDuplicateError)


def ingredients_validator(data):
    """Валидатор ингредиентов"""
    limits = {
        'ingredients': 30,
        'amount': 10_000
    }

    ingredients_set = set(
        ingredient['id'] for ingredient in data
    )

    if len(data) != len(ingredients_set):
        raise IngredientDuplicateError

    if len(data) > limits['ingredients']:
        raise IngredientLimitError(limits['ingredients'])

    for ingredient in data:
        if ingredient['amount'] > limits['amount']:
            raise IngredientLimitError(
                limit_numb=limits['amount'],
                detail=_('Превышено количество ингредиента')
            )

    return True


def tags_validator(data):
    """Валидатор тегов"""
    if len(set(data)) != len(data):
        raise TagDuplicateError

    return True


def subscription_validator(data):
    """Валидатор подписки"""
    user = data.get('user')
    author = data.get('author')

    if user == author:
        raise SubscriptionYouError

    if user.subscriber.filter(
            user=user, author=author).exists():
        raise SubscriptionExistsError

    return True


def favorite_validator(data):
    """Валидатор подписки"""
    user = data.get('user')
    recipe = data.get('recipe')

    if user.favorites.filter(recipe=recipe).exists():
        raise FavoriteExistsError

    return True


def shopping_cart_validator(data):
    """Валидатор корзины рецептов"""
    user = data.get('user')
    recipe = data.get('recipe')

    if user.cart.filter(recipe=recipe).exists():
        raise ShoppingCartExistsError

    return True

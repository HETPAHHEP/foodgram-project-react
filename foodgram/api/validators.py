from django.utils.translation import gettext_lazy as _

from .exceptions import (FavoriteExistsError, IngredientDuplicateError,
                         IngredientLimitError, ShoppingCartExistsError,
                         SubscriptionExistsError, SubscriptionYouError,
                         TagDuplicateError)


class IngredientsValidator:
    """Валидатор ингредиентов"""
    message = _('Ингредиенты недействительны')
    limits = {
        'ingredients': 30,
        'amount': 10_000
    }

    def __init__(self, data, message=None):
        self.data = data
        if message:
            self.message = message

    def __call__(self):
        return self.validate(self.data)

    def validate(self, data):
        ingredients_set = set(
            ingredient['id'] for ingredient in data
        )

        if len(data) != len(ingredients_set):
            raise IngredientDuplicateError

        if len(data) > self.limits['ingredients']:
            raise IngredientLimitError(self.limits['ingredients'])

        for ingredient in data:
            if ingredient['amount'] > self.limits['amount']:
                raise IngredientLimitError(
                    limit_numb=self.limits['amount'],
                    detail=_('Превышено количество ингредиента')
                )

        return True


class TagsValidator:
    """Валидатор тегов"""
    message = _('Теги недействительны')

    def __init__(self, data, message=None):
        self.data = data
        if message:
            self.message = message

    def __call__(self):
        return self.validate(self.data)

    @staticmethod
    def validate(data):
        print()
        if len(set(data)) != len(data):
            raise TagDuplicateError

        return True


class SubscriptionValidator:
    """Валидатор подписки"""
    message = _('Подписка недействительна')

    def __init__(self, data, message=None):
        self.data = data
        if message:
            self.message = message

    def __call__(self):
        return self.validate(self.data)

    @staticmethod
    def validate(data):
        user = data.get('user')
        author = data.get('author')

        if user == author:
            raise SubscriptionYouError

        if user.subscriber.filter(
                user=user, author=author).exists():
            raise SubscriptionExistsError

        return True


class FavoriteValidator:
    """Валидатор подписки"""
    message = _('Невозможно добавить в избранное')

    def __init__(self, data, message=None):
        self.data = data
        if message:
            self.message = message

    def __call__(self):
        return self.validate(self.data)

    @staticmethod
    def validate(data):
        user = data.get('user')
        recipe = data.get('recipe')

        if user.favorites.filter(recipe=recipe).exists():
            raise FavoriteExistsError

        return True


class ShoppingCartValidator:
    """Валидатор корзины рецептов"""
    message = _('Невозможно добавить в корзину')

    def __init__(self, data, message=None):
        self.data = data
        if message:
            self.message = message

    def __call__(self):
        return self.validate(self.data)

    @staticmethod
    def validate(data):
        user = data.get('user')
        recipe = data.get('recipe')

        if user.cart.filter(recipe=recipe).exists():
            raise ShoppingCartExistsError

        return True

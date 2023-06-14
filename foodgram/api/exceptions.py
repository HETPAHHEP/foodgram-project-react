from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError


class SubscriptionYouError(ValidationError):
    """Ошибка при попытке подписаться на себя"""
    default_detail = _('Подписка на себя невозможна')
    default_code = 'errors'
    status_code = status.HTTP_400_BAD_REQUEST


class SubscriptionExistsError(ValidationError):
    """
    Ошибка при существовании подписки на автора.
    Невозможно подписаться повторно.
    """
    default_detail = _('Подписка на автора уже осуществлена')
    default_code = 'errors'
    status_code = status.HTTP_400_BAD_REQUEST


class SubscriptionDoesntExistError(ValidationError):
    """
    Ошибка при попытке отписаться от автора,
    на которого не была осуществлена подписка
    """
    default_code = 'errors'
    default_detail = {
        f'{default_code}': _('Пользователь не был подписан на автора')
    }
    status_code = status.HTTP_400_BAD_REQUEST


class TagsIngredientsRequiredError(ValidationError):
    """Невозможно создать рецепт без тегов или ингредиентов"""
    default_detail = _('Невозможно создать рецепт без тегов или ингредиентов')
    default_code = 'tags'
    status_code = status.HTTP_400_BAD_REQUEST


class TagDuplicateError(ValidationError):
    """Невозможно создать рецепт с одинаковыми тегами"""
    default_detail = _('Теги должны быть уникальны')
    default_code = 'tags'
    status_code = status.HTTP_400_BAD_REQUEST


class TagDoesntExistError(ValidationError):
    """Невозможно создать рецепт с несуществующим тегом"""
    default_detail = _('Данного тега не существует')
    default_code = 'tags'
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, non_existent_tag=None):
        if non_existent_tag:
            self.default_detail += f': {non_existent_tag}'

        super().__init__(detail=self.default_detail, code=self.default_code)


class IngredientDuplicateError(ValidationError):
    """Невозможно создать рецепт с одинаковыми ингредиентами"""
    default_detail = _('Ингредиенты должны быть уникальны')
    default_code = 'ingredients'
    status_code = status.HTTP_400_BAD_REQUEST


class IngredientLimitError(ValidationError):
    """Ограничено количество одного ингредиента"""
    default_detail = _('Превышено количество ингредиентов')
    default_code = 'ingredients'
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, limit_numb=None, detail=None):
        if limit_numb:
            if detail:
                self.default_detail = detail + f': {limit_numb}'
            else:
                self.default_detail = _(
                    f'Превышено количество ингредиентов: {limit_numb}'
                )

        super().__init__(detail=self.default_detail, code=self.default_code)


class RecipeExistsError(ValidationError):
    """
    Невозможно создать рецепт с уже имеющимся именем,
    если у автора он есть.
    """
    default_detail = {"detail": f'{_("Рецепт с таким именем уже существует")}'}
    default_code = 'name'
    status_code = status.HTTP_400_BAD_REQUEST


class FavoriteExistsError(ValidationError):
    """
    Невозможно добавить рецепт в избранного,
    если автора уже сделал это.
    """
    default_code = 'errors'
    default_detail = {f"{default_code}": _("Рецепт уже добавлен в избранное")}
    status_code = status.HTTP_400_BAD_REQUEST


class ShoppingCartExistsError(ValidationError):
    """
    Невозможно добавить рецепт в избранного,
    если автора уже сделал это.
    """
    default_code = 'errors'
    default_detail = {f"{default_code}": _("Рецепт уже добавлен в корзину")}
    status_code = status.HTTP_400_BAD_REQUEST


class FavoriteDoesntExistError(ValidationError):
    """
    Невозможно убрать рецепт из корзины,
    если его там нет.
    """
    default_code = 'errors'
    default_detail = {
        f"{default_code}": _("Рецепт не был добавлен в избранное")
    }
    status_code = status.HTTP_400_BAD_REQUEST


class ShoppingCartDoesntExistError(ValidationError):
    """
    Невозможно добавить рецепт в корзину,
    если автора уже сделал это.
    """
    default_code = 'errors'
    default_detail = {f"{default_code}": _("Рецепт уже добавлен в корзину")}
    status_code = status.HTTP_400_BAD_REQUEST

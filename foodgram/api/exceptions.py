from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class SubscriptionYouError(APIException):
    """Ошибка при попытке подписаться на себя"""
    default_detail = _('Подписка на себя невозможна')
    default_code = 'errors'
    status_code = status.HTTP_400_BAD_REQUEST


class SubscriptionExistsError(APIException):
    """
    Ошибка при существовании подписки на автора.
    Невозможно подписаться повторно.
    """
    default_detail = _('Подписка на автора уже осуществлена')
    default_code = 'errors'
    status_code = status.HTTP_400_BAD_REQUEST


class SubscriptionDoesntExistError(APIException):
    """
    Ошибка при попытке отписаться от автора,
    на которого не была осуществлена подписка
    """
    default_detail = _('Пользователь не был подписан на автора')
    default_code = 'errors'
    status_code = status.HTTP_404_NOT_FOUND

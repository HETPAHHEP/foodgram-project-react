from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class FollowYouError(APIException):
    """Ошибка при подписки на себя"""
    default_detail = _('Подписка на себя невозможна')
    default_code = 'errors'
    status_code = status.HTTP_400_BAD_REQUEST


class FollowExistsError(APIException):
    """
    Ошибка при существовании подписки на автора.
    Невозможно подписаться повторно.
    """
    default_detail = _('Подписка на автора уже осуществлена')
    default_code = 'errors'
    status_code = status.HTTP_400_BAD_REQUEST

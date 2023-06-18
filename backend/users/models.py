from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name=_('Почта')
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name=_('Имя')
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name=_('Фамилия')
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписок пользователей на авторов"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name=_('Пользователь')
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name=_('Автор')
    )

    class Meta:
        verbose_name = _('Подписчик')
        verbose_name_plural = _('Подписчики')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_followers'
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.author}'

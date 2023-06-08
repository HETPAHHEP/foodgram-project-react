from django.contrib.auth.models import AbstractUser, BaseUserManager
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
    bio = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name=_('О себе')
    )
    avatar = models.ImageField(
        upload_to='media/users/avatars/',
        blank=True, null=True,
        verbose_name=_('Фото')
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок пользователей на авторов"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=_('Пользователь')
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Автор')
    )

    class Meta:
        verbose_name = _('Подписчик')
        verbose_name_plural = _('Подписчики')
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique_followers'),
        ]

    def __str__(self):
        return f'{self.user} - {self.author}'

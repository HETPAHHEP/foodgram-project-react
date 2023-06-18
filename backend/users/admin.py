from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Subscription

CustomUser = get_user_model()


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Отображение пользователей"""
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    list_filter = ['email', 'username']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Отображение подписок пользователей"""
    list_display = ['id', 'follower_username', 'author_username']

    def follower_username(self, obj):
        return obj.user.username

    def author_username(self, obj):
        return obj.author.username

    follower_username.short_description = _('Подписчик')
    author_username.short_description = _('Автор')

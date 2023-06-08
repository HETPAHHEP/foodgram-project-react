from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Follow

CustomUser = get_user_model()


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    list_filter = ['email', 'username']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower_username', 'author_username']

    def follower_username(self, obj):
        return obj.user.username

    def author_username(self, obj):
        return obj.author.username

    follower_username.short_description = _('Подписчик')
    author_username.short_description = _('Автор')

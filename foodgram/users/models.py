from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(max_length=160, blank=True, null=True)
    avatar = models.ImageField(upload_to='media/users/', blank=True, null=True)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок пользователей на авторов"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')

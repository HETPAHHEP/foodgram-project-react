from django.contrib.auth import get_user_model
from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Tag

CustomUser = get_user_model()


class RegisterUserSerializer(BaseUserRegistrationSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(max_length=150, min_length=8, write_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ['first_name', 'username', 'last_name', 'email', 'password']


class CustomUserSerializer(UserSerializer):
    """Сериализатор для данных пользователей"""

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ['email', 'id', 'username', 'first_name', 'last_name']


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = '__all__'

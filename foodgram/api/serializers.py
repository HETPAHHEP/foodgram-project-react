from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers

CustomUser = get_user_model()


class RegisterUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(
        max_length=150,
        min_length=8,
        write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецептов"""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image',
            'text', 'cooking_time'
        ]

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.favorites.filter(recipe=obj, user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.cart.filter(recipe=obj, user=user).exists()
        return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецептов"""
    class Meta:
        model = Recipe
        fields = [
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        ]

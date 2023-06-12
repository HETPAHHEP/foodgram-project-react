from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import Subscription

from .exceptions import SubscriptionExistsError, SubscriptionYouError

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
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed'
        ]
        read_only_fields = ['is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return bool(
            user.is_authenticated and user != obj and
            user.subscriber.filter(author=obj).exists()
        )


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


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """Простой сериализатор для рецептов"""
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецептов"""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
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
    # tags = serializers.PrimaryKeyRelatedField(
    # many=True, queryset=Tag.objects.all()
    # )

    class Meta:
        model = Recipe
        fields = [
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        ]


class SubscriptionListSerializer(CustomUserSerializer):
    """Сериализатор подписок"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes_serializer = SimpleRecipeSerializer

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + [
            'recipes', 'recipes_count'
        ]
        read_only_fields = [
            'email', 'id', 'username',
            'first_name', 'last_name'
        ]

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]

        serializer = self.recipes_serializer(
            recipes, many=True, read_only=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки"""
    list_serializer = SubscriptionListSerializer

    class Meta:
        model = Subscription
        fields = ['user', 'author']

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')

        if user == author:
            raise SubscriptionYouError

        if user.subscriber.filter(
                user=user, author=author).exists():
            raise SubscriptionExistsError

        return data

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)

    def to_representation(self, instance):
        return self.list_serializer(
            instance=instance.author, context=self.context).data

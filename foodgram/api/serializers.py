from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import Subscription

from .exceptions import TagsIngredientsRequiredError
from .validators import (IngredientsValidator, SubscriptionValidator,
                         TagsValidator)

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
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов рецепта"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class CreateIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов в рецепт"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """Простой сериализатор для рецептов"""

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецептов"""
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        ]

    def get_ingredients(self, obj):
        ingredients = obj.ingredient.all()
        serializer = IngredientRecipeSerializer(ingredients, many=True)
        return serializer.data

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
    ingredients = CreateIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = [
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        ]

    def validate(self, data):
        validated_data = super().validate(data)

        ingredients = data.get('ingredients')
        tags = data.get('tags')

        if not tags or not ingredients:
            raise TagsIngredientsRequiredError

        if IngredientsValidator(data=ingredients)() and \
                TagsValidator(data=tags)():
            return validated_data

    @atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            ingredient = ingredient_data['id']
            amount = ingredient_data['amount']
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )

        recipe.tags.set(tags_data)

        return recipe

    @atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags_data = validated_data.pop('tags', None)

        recipe = super().update(instance, validated_data)

        if ingredients_data:
            recipe.ingredients.delete()

            for ingredient_data in ingredients_data:
                ingredient = ingredient_data['id']
                amount = ingredient_data['amount']
                RecipeIngredient.objects.create(
                    recipe=recipe, ingredient=ingredient, amount=amount
                )

        if tags_data:
            recipe.tags.delete()
            recipe.tags.set(tags_data)

        recipe.save()
        return recipe

    def to_representation(self, instance):
        recipe = RecipeReadSerializer(
            instance=instance, context=self.context).data
        del recipe['author']

        return recipe


class SubscriptionListSerializer(CustomUserSerializer):
    """Сериализатор подписок"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

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

        serializer = SimpleRecipeSerializer(
            recipes, many=True, read_only=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки"""

    class Meta:
        model = Subscription
        fields = ['user', 'author']

    def validate(self, data):
        if SubscriptionValidator(data=data)():
            return data

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)

    def to_representation(self, instance):
        return SubscriptionListSerializer(
            instance=instance.author, context=self.context
        ).data

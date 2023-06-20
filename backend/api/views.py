from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Ingredient, Recipe, RecipeIngredient, ShoppingCart,
                            Tag)

from .exceptions import (FavoriteDoesntExistError, RecipeExistsError,
                         ShoppingCartDoesntExistError,
                         SubscriptionDoesntExistError, SubscriptionYouError)
from .filters import IngredientFilter, RecipeFilter
from .paginators import CustomPagination
from .permissions import IsOwnerAdminOrReadOnly
from .serializers import (FavoritesAddSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          ShoppingCartAddSerializer,
                          SubscriptionCreateSerializer,
                          SubscriptionListSerializer, TagSerializer)
from .services.service_download_cart import download_cart_pdf

CustomUser = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Взаимодействие с пользователями и подписками"""
    pagination_class = CustomPagination

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Получить все подписки пользователя"""
        user = request.user
        paginated_subscriptions = self.paginate_queryset(
            CustomUser.objects.filter(subscription__user=user),
        )
        serializer = SubscriptionListSerializer(
            paginated_subscriptions, many=True, context={'request': request})

        return self.get_paginated_response(data=serializer.data)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Подписаться на пользователя"""
        author = get_object_or_404(CustomUser, id=id)
        user = request.user

        serializer = SubscriptionCreateSerializer(
            data={'author': author.id, 'user': user.id},
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Подписываемся на автора
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        """Отписаться от пользователя"""
        author = get_object_or_404(CustomUser, id=id)
        user = request.user

        if user == author:
            raise SubscriptionYouError(
                detail=_('Невозможно отписаться от себя')
            )

        subscription_check = user.subscriber.filter(author=author)
        if subscription_check.exists():
            subscription_check.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise SubscriptionDoesntExistError


class TagViewSet(ReadOnlyModelViewSet):
    """Вывод всех тегов или только конкретного"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None  # Убирает пагинацию по умолчанию


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вывод всех ингредиентов или только конкретного"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    search_fields = ['^name']
    pagination_class = None  # Убирает пагинацию по умолчанию


class RecipeViewSet(ModelViewSet):
    """Вывод и изменение рецептов"""
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action in ('delete', 'update'):
            self.permission_classes = [IsOwnerAdminOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            raise RecipeExistsError

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Скачать PDF с ингредиентами рецептов в корзине"""
        user = request.user

        shopping_list = RecipeIngredient.objects.filter(
            recipe__in_cart__user=user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        if shopping_list:
            buffer = download_cart_pdf(shopping_list)

            return FileResponse(
                buffer,
                as_attachment=True,
                filename=f"shopping_list_{user}.pdf"
            )

        return NotFound(detail=_('В корзине ничего нет'), code='errors')

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Добавить рецепт в корзину"""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'recipe': recipe.id, 'user': user.id}

        serializer = ShoppingCartAddSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        """Удалить рецепт из корзины"""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if get_object_or_404(ShoppingCart, user=user, recipe=recipe).delete():
            return Response(status=status.HTTP_204_NO_CONTENT)

        cart_check = user.cart.filter(recipe=recipe)
        if cart_check.exists():
            cart_check.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise ShoppingCartDoesntExistError

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Добавить рецепт в избранное"""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'recipe': recipe.id, 'user': user.id}

        serializer = FavoritesAddSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

    @favorite.mapping.delete
    def favorite_delete(self, request, pk):
        """Удалить рецепт из избранного"""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        favorite_check = user.favorites.filter(recipe=recipe)
        if favorite_check.exists():
            favorite_check.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise FavoriteDoesntExistError

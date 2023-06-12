from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .exceptions import SubscriptionDoesntExistError, SubscriptionYouError
from .paginators import CustomPagination
from .permissions import IsOwnerAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, SubscriptionListSerializer,
                          SubscriptionSerializer, TagSerializer)

CustomUser = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Взаимодействие с пользователями и подписками"""
    subscription_serializer = SubscriptionListSerializer
    create_subscription_serializer = SubscriptionSerializer
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
        serializer = self.subscription_serializer(
            paginated_subscriptions, many=True, context={'request': request})

        return self.get_paginated_response(data=serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Подписаться на пользователя или отписаться от него"""
        author = get_object_or_404(CustomUser, id=id)
        user = request.user

        if request.method == 'POST':
            serializer = self.create_subscription_serializer(
                data={'author': author.id, 'user': user.id},
                context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # Подписываемся на автора
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )

        if request.method == 'DELETE':
            if user == author:
                raise SubscriptionYouError(
                    detail=_('Невозможно отписаться от себя')
                )

            if user.subscriber.filter(author=author).exists():
                user.subscriber.filter(author=author).delete()  # Отписка
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

    pagination_class = None  # Убирает пагинацию по умолчанию


class RecipeViewSet(ModelViewSet):
    """Вывод и изменение рецептов"""
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination

    permission_classes = []  # По умолчанию: AllowAny

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
        serializer.save(author=self.request.user)

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Follow

from .exceptions import FollowExistsError, FollowYouError
from .paginators import CustomPaginationRecipe
from .permissions import IsOwnerAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)

CustomUser = get_user_model()


class FollowUserView(APIView):
    """Подписаться на автора"""
    serializer_class = ''

    def post(self, request, user_id):
        author = CustomUser.objects.filter(id=user_id).first()

        if author.exists():
            if request.user == author:
                raise FollowYouError

            if request.user.follower.objects.filter(
                    user=request.user, author=author).exists():
                raise FollowExistsError

            Follow(user=request.user, author=author)

            return Response()  # TODO: сериализатор с подробной инфой юзера

        raise exceptions.NotFound(
            detail=_('Страница не найдена'),
            code='detail'
        )

        # return Response(data={
        #     'detail': 'Страница не найдена'
        # }, status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(APIView):
    """Отписаться от автора"""
    def delete(self, request, user_id):
        author = CustomUser.objects.filter(id=user_id).first()

        if author.exists():
            if request.user == author:
                raise FollowYouError(detail=_('Невозможно отписаться от себя'))


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
    pagination_class = CustomPaginationRecipe

    permission_classes = []  # По умолчанию: AllowAny

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return RecipeWriteSerializer
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action in ('delete', 'update'):
            self.permission_classes = [IsOwnerAdminOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

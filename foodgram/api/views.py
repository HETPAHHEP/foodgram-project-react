from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Tag, Ingredient
from users.models import Follow

from .exceptions import FollowExistsError, FollowYouError
from .serializers import TagSerializer, IngredientSerializer

CustomUser = get_user_model()


class FollowUserView(APIView):
    """Подписаться на автора"""
    serializer_class = ''

    def post(self, request, user_id):
        author = CustomUser.objects.filter(id=user_id).first()

        if author.exists():
            if request.user == author:
                raise FollowYouError

            if Follow.objects.filter(user=request.user, author=author).exists():
                raise FollowExistsError

            Follow(user=request.user, author=author)

            return Response()  # TODO: Добавить сериализатор с подробной инфой юзера

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


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вывод всех ингредиентов или только конкретного"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

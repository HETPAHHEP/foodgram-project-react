from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'tags', views.TagViewSet, basename='tags')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

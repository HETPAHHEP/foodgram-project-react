from django.urls import include, path
from rest_framework import routers

from . import views

# router = routers.DefaultRouter()
# router.register(r'')


urlpatterns = [
    # path('auth/signup/', views.RegisterUserView.as_view(), name='registration'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]

from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from users.models import CustomUser


class RegisterUserSerializer(BaseUserRegistrationSerializer):
    password = serializers.CharField(max_length=150, min_length=8, write_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ['first_name', 'username', 'last_name', 'email', 'password']

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     username = attrs.get('username')

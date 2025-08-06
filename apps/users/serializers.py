"""
Custom user serializers for Djoser authentication.

These serializers extend Djoser's default user creation and user detail serializers
to include specific fields like email, first name, and last name.
"""

from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for user registration.
    """

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomUserSerializer(BaseUserSerializer):
    """
    Serializer for user detail retrieval.
    Extends Djoser's `UserSerializer` 
    """

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')

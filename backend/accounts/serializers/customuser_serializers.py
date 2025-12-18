from accounts.models import CustomUser
from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ("id", "username", "password", "email", "first_name", "last_name", "phone_number")


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ("id", "username", "email", "first_name", "last_name", "phone_number")


class CustomCurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ("id", "username", "email", "first_name", "last_name", "phone_number")

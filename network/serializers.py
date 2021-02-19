from rest_framework import serializers
from .models import CustomUser, Post, Like

from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ('is_active', 'is_staff', 'date_joined', 'last_login', 'groups',
                   'user_permissions', 'is_superuser')

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = 'id', 'text',

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data["user"] = user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ('date', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data["user"] = user
        return super().create(validated_data)


from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account import models


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SlaveUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SlaveUser
        exclude = ['password']


class LoginTokenObtainPairSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError({
                'detail': 'User account is not verified.'
            })

        refresh = self.get_token(self.user)

        # ToDo can try another way
        context = {
            'request': self.context.get('requests')
        }
        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(self.user, context=context)
        })

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

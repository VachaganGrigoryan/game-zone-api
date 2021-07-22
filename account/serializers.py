from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account import models


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = models.SlaveUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def check_email_and_username(self, data):
        errors = {}

        if models.SlaveUser.objects.filter(email=data['email']):
            errors['email'] = ["User with this email already exists."]

        if models.SlaveUser.objects.filter(username=data['username']):
            errors["username"] = ["User with this username already exists."]

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SlaveUserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(required=False)
    avatar = serializers.ImageField(source='profile.avatar')
    banner = serializers.ImageField(source='profile.banner')
    bio = serializers.CharField(source='profile.bio')
    app_notify = serializers.BooleanField(source='profile.app_notify')
    email_notify = serializers.BooleanField(source='profile.email_notify')

    class Meta:
        model = models.SlaveUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'is_verified',
            'profile',
            "avatar",
            "banner",
            "bio",
            "app_notify",
            "email_notify",
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in profile_data.items():
            setattr(instance.profile, attr, value)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.profile.save()
        instance.save()
        return instance


class MeSerializer(UserSerializer):
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

        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(self.user, context=self.context).data
        })

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class ForgetPassword(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class ForgetPasswordVerified(serializers.Serializer):
    code = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=128)

from datetime import date

import django.db.utils
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, mixins, viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from account import models
from account import serializers
from core.email_sender import send_multi_format_email


class SignUp(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            username = serializer.data['username']
            password = serializer.data['password']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']

            must_validate_email = getattr(settings, 'AUTH_EMAIL_VERIFICATION', True)

            try:
                user = models.SlaveUser.objects.get(email=email, username=username)
                if user.is_verified:
                    content = {'detail': 'Email address already taken.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                try:
                    signup_code = models.SignUpCode.objects.get(user=user)
                    signup_code.delete()
                except models.SignUpCode.DoesNotExist:
                    pass
            except models.SlaveUser.DoesNotExist:
                user = models.SlaveUser.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

            if not must_validate_email:
                user.is_verified = True

                send_multi_format_email(
                    'welcome_email',
                    {'email': user.email},
                    target_email=user.email
                )
                user.save()

            if must_validate_email:
                ip_address = '0.0.0.0'  # self.request.META.get('REMOTE_ADDR', '0.0.0.0') ToDo need to fix
                signup_code = models.SignUpCode.objects.create_signup_code(user, ip_address)
                signup_code.send_signup_mail()

            return Response(serializers.UserSerializer(user), status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpVerify(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, f=None):
        code = request.GET.get('code', '')

        verified = models.SignUpCode.objects.set_user_is_verified(code)

        if verified:
            try:
                signup_code = models.SignUpCode.objects.get(code=code)
                signup_code.delete()
            except models.SignUpCode.DoesNotExist:
                pass
            content = {'success': 'Email address is verified.'}
            return Response(content, status=status.HTTP_200_OK)

        content = {'detail': 'Unable to verify user.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenObtainPair(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginTokenObtainPairSerializer



class Logout:
    pass

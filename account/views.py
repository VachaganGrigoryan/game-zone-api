from datetime import date

# import django.db.utils
from django.conf import settings
# from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, viewsets, generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from . import models, serializers
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
                    content = {'detail': 'User with that email and username address already taken.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                try:
                    signup_code = models.SignUpCode.objects.get(user=user)
                    signup_code.delete()
                except models.SignUpCode.DoesNotExist:
                    pass
            except models.SlaveUser.DoesNotExist:

                serializer.check_email_and_username(data={
                    'email': email,
                    'username': username
                })

                user = models.SlaveUser.objects.create_user(
                    email=email,
                    username=username
                )

            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
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

            return Response(serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpVerify(APIView):
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


class Logout(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Accounts(viewsets.ModelViewSet):
    queryset = models.SlaveUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


class Me(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MeSerializer

    def get(self, request, f=None):
        return Response(self.serializer_class(request.user, context={"request": request}).data)


class ForgotPassword(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ForgetPassword

    def post(self, request, f=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = models.SlaveUser.objects.get(email=email)

                models.PasswordResetCode.objects.filter(user=user).delete()

                if user.is_verified and user.is_active:
                    password_reset_code = models.PasswordResetCode.objects.create_password_reset_code(user=user)
                    password_reset_code.send_password_reset_email()
                    content = {'email': email}
                    return Response(content, status.HTTP_201_CREATED)
            except models.SlaveUser.DoesNotExist:
                pass

            content = {'detail': 'Password reset not allowed.'}
            return Response(content, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ForgetPasswordVerify(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, f=None):
        code = request.GET.get('code', '')
        print(code)
        try:
            forgot_password = models.PasswordResetCode.objects.get(code=code)

            diff_date = date.today() - forgot_password.created_at.date()

            if diff_date.days > models.PasswordResetCode.objects.get_expiry_period():
                forgot_password.delete()
                raise models.PasswordResetCode.DoesNotExist()

            content = {'success': 'Email address verified.'}
            return Response(content, status=status.HTTP_200_OK)
        except models.PasswordResetCode.DoesNotExist:
            content = {'detail': 'Unable to verify user.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordVerified(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ForgetPasswordVerified

    def post(self, request, f=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data['code']
            password = serializer.data['password']

            try:
                password_reset_code = models.PasswordResetCode.objects.get(code=code)
                password_reset_code.user.set_password(password)
                password_reset_code.user.save()

                password_reset_code.delete()

                content = {'success': 'Password reset.'}
                return Response(content, status=status.HTTP_200_OK)
            except models.PasswordResetCode.DoesNotExist:
                content = {'detail': 'Unable to verify user.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class SimpleApI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    # https://github.com/sjlouji/Medium-Django-Rest-Framework-JWT-auth-login-register
    # https://medium.com/python-in-plain-english/django-rest-framework-jwt-auth-with-login-and-register-77f830cd8789
    # https://medium.com/python-in-plain-english/django-rest-framework-jwt-auth-with-drf-e13ccde9e68f
    # https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8
    # https://medium.com/django-rest/django-rest-framework-login-and-register-user-fd91cf6029d5
    # https://github.com/egitimplus/medium/blob/part8/medium/settings.py
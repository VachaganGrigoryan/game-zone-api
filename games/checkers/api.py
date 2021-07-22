from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, mixins
from .serializers import GameBoardSerializer, HistoriesSerializer
from .models import GameBoard


class GameBoardApi(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameBoardSerializer
    queryset = GameBoard.objects.all()
    # lookup_fields = ('id', 'owner', 'winner')
    #
    # def get(self, request, pk=None):
    #     # return Response({'message': 'Hello, DashBoard!', "username": self.request.user.username})
    #     return Response(self.queryset.all())


class CreateApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class DeleteApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class FinishApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class JoinApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class ReadyApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class PlayApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class PauseApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)


# class DashboardApi(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     def get(self, request):
#         content = {'message': 'Hello, DashBoard!', "username": self.request.user.username}
#         return Response(content)


# class RegisterApi(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args,  **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "message": "User Created Successfully.  Now perform Login to get your token",
#         })


    # https://github.com/sjlouji/Medium-Django-Rest-Framework-JWT-auth-login-register

    # https://medium.com/python-in-plain-english/django-rest-framework-jwt-auth-with-login-and-register-77f830cd8789
    # https://medium.com/python-in-plain-english/django-rest-framework-jwt-auth-with-drf-e13ccde9e68f
    # https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8
    # https://medium.com/django-rest/django-rest-framework-login-and-register-user-fd91cf6029d5
    # https://github.com/egitimplus/medium/blob/part8/medium/settings.py


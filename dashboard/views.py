from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response


class DashBoardViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        content = {'message': 'Hello, DashBoard!', "username": self.request.user.username}
        return Response(content)
from django.urls import path, include
from .api import DashboardApi, RegisterApi, ListUsers
from .views import dashboard


urlpatterns = [
    path("dashboard/", DashboardApi.as_view(), name="dashboard"),
    path('register', RegisterApi.as_view()),
    path('users', ListUsers.as_view())
]

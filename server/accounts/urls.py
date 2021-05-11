from django.urls import path, include
from .api import DashboardApi, RegisterApi, ListUsersApi
from .views import dashboard


urlpatterns = [
    path("dashboard/", DashboardApi.as_view(), name="dashboard"),
    path('register', RegisterApi.as_view(), name="register"),
    path('users', ListUsersApi.as_view(), name="users")
]

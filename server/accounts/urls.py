from django.urls import path, include
from .api import DashboardApi, RegisterApi
from .views import dashboard


urlpatterns = [
    path("api/dashboard/", DashboardApi.as_view(), name="dashboard"),
    path('api/register', RegisterApi.as_view()),
]

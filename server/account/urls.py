from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from account import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='account-signup'),
    path('signup/verify/', views.SignUpVerify.as_view(), name='account-signup-verify'),

    path('login/', views.LoginTokenObtainPair.as_view(), name='account-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='account-login-refresh'),
    path('logout/', views.Logout.as_view(), name='account-logout'),


]

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from . import views

urlpatterns = [

    path('signup/', views.SignUp.as_view(), name='account-signup'),
    path('signup/verify/', views.SignUpVerify.as_view(), name='account-signup-verify'),

    path('login/', views.LoginTokenObtainPair.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='account-login-refresh'),
    path('logout/', views.Logout.as_view(), name='account-logout'),

    path('password/reset/', views.ForgotPassword.as_view(), name='account-forgot-password'),
    path('password/reset/verify/', views.ForgetPasswordVerify.as_view(), name='account-forgot-password-verify'),
    path('password/reset/verified/', views.ForgetPasswordVerified.as_view(), name='account-forgot-password-verified'),

    path('profiles/', views.Accounts.as_view({
        'get': 'list'
    }), name='accounts'),
    path('profiles/me/', views.Me.as_view(), name='account-me'),
    path('profiles/<str:username>/', views.Accounts.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update'
    }), name='account-detail'),

]

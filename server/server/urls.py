"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt import views as jwt_views

# from todo import views
#
# router = routers.DefaultRouter()
# router.register(r'todos', views.TodoView, 'todo')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('redoc/', TemplateView.as_view(template_name='redoc.html', extra_context={'schema_url': 'openapi-schema'}), name='redoc'),
    path('api/docs/', TemplateView.as_view(template_name='swagger-ui.html', extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('openapi/', get_schema_view(title="Checkers API", description="API for checkers …", version="1.0.0"), name='openapi-schema'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('api/dashboard/', include('dashboard.urls')),
    path('api/account/', include('accounts.urls')),
    path('api/checkers/', include('checkers.urls')),
]

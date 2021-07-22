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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account import urls as account_urls

schema_view = get_schema_view(
   openapi.Info(
      title="Game Zone API",
      default_version='v0',
      description="Game Zone API documentation",
      terms_of_service="",
      contact=openapi.Contact(email="vachagan.grigoryan.it@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


class DefaultRouter(routers.DefaultRouter):
    def extend(self, app_router):
        self.registry.extend(app_router.registry)


router = DefaultRouter()
# router.extend(account_urls)
# router.extend(marketplace_urls)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),

    path('api/accounts/', include('account.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/checkers/', include('games.checkers.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger.<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

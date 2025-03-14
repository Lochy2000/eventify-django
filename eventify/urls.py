"""
URL configuration for eventify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from dj_rest_auth.jwt_auth import get_refresh_view
from eventify.views import root_route, logout_route
from .views import csrf

urlpatterns = [
    path('', root_route, name='root'),
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/logout/', logout_route, name='logout'),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api-auth/', include('rest_framework.urls')),

    path('api/csrf/', csrf, name='csrf'),

    path('api/', include('followers.urls')),
    path('api/', include('favorites.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('likes.urls')),
    path('api/', include('events.urls')),
    path('api/', include('profiles.urls')),
]

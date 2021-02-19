"""Demo_Rest URL Configuration

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
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken import views
from network.views import UserRegistrationView, PostView, LikeView, AnalyticView, ActivityView,LogoutView


router = routers.DefaultRouter()
router.register(r"reg", UserRegistrationView)
router.register(r"post", PostView)
router.register(r"like", LikeView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, "app"))),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout', LogoutView.as_view(), name='logout'),
    path('api/analitic', AnalyticView.as_view(), name='analytic'),
    path('api/activity', ActivityView.as_view(), name='activity'),
    path('api/token-auth', views.obtain_auth_token)

]



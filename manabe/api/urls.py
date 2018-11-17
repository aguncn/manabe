# coding=utf8
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_views
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet, base_name="user")
router.register(r'deploypools', views.DeployPoolViewSet, base_name="deploypool")
router.register(r'servers', views.ServerViewSet, base_name="server")
router.register(r'apps', views.AppViewSet, base_name="app")

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', rest_views.obtain_auth_token),
]
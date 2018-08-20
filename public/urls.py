from django.urls import path

from .get_env import get_env
from .get_app import get_app

app_name = 'public'

urlpatterns = [
    path('get-env/', get_env, name='get-env'),
    path('get-app/', get_app, name='get-app'),
]
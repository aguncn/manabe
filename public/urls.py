from django.urls import path

from .get_env import get_env

app_name = 'public'

urlpatterns = [
    path('get-env/', get_env, name='get-env'),
]
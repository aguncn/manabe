from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import ServerInputCreateView, \
    ServerInputUpdateView, \
    ServerInputDetailView, \
    ServerInputListView

app_name = 'serverinput'

urlpatterns = [
    path('create/',
         login_required(ServerInputCreateView.as_view()),
         name='create'),
    path(r'list/',
         login_required(ServerInputListView.as_view()),
         name='list'),
    path(r'edit/<slug:pk>/',
         login_required(ServerInputUpdateView.as_view()),
         name='edit'),
    path(r'view/<slug:pk>/',
         login_required(ServerInputDetailView.as_view()),
         name='detail'),
]
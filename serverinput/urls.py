from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import ServerInputCreateView, ServerInputUpdateView, ServerInputDetailView, ServerInputListView

app_name = 'serverinput'

urlpatterns = [
    path('serverinput/create/', login_required(ServerInputCreateView.as_view()),
         name='serverinput-create'),
    path(r'serverinput/list/', login_required(ServerInputListView.as_view()),
         name='serverinput-list'),
    path(r'serverinput/edit/<slug:pk>/', login_required(ServerInputUpdateView.as_view()),
         name='serverinput-edit'),
    path(r'serverinput/view/<slug:pk>/', login_required(ServerInputDetailView.as_view()),
         name='serverinput-detail'),

]
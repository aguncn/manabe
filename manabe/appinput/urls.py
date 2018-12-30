from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppInputCreateView, \
    AppInputUpdateView, \
    AppInputDetailView, \
    AppInputListView

app_name = 'appinput'

urlpatterns = [
    path('create/', login_required(AppInputCreateView.as_view()),
         name='create'),
    path('list/', login_required(AppInputListView.as_view()),
         name='list'),
    path('edit/<slug:pk>/', login_required(AppInputUpdateView.as_view()),
         name='edit'),
    path('view/<slug:pk>/', login_required(AppInputDetailView.as_view()),
         name='detail'),
]
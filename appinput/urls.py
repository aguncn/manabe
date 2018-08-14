from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppInputCreateView, AppInputUpdateView, AppInputDetailView, AppInputListView

app_name = 'appinput'

urlpatterns = [
    path('appinput/create/', login_required(AppInputCreateView.as_view()),
         name='appinput-create'),
    path(r'appinput/list/', login_required(AppInputListView.as_view()),
         name='appinput-list'),
    path(r'appinput/edit/<slug:pk>/', login_required(AppInputUpdateView.as_view()),
         name='appinput-edit'),
    path(r'appinput/view/<slug:pk>/', login_required(AppInputDetailView.as_view()),
         name='appinput-detail'),

]
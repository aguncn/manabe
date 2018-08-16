from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import DeployCreateView, DeployUpdateView, DeployDetailView, DeployListView

app_name = 'deploy'

urlpatterns = [
    path('create/', login_required(DeployCreateView.as_view()),
         name='create'),
    path(r'list/', login_required(DeployListView.as_view()),
         name='list'),
    path(r'edit/<slug:pk>/', login_required(DeployUpdateView.as_view()),
         name='edit'),
    path(r'view/<slug:pk>/', login_required(DeployDetailView.as_view()),
         name='detail'),

]
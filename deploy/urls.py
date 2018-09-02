from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import DeployCreateView, DeployUpdateView, DeployDetailView, DeployListView, jenkins_build, jenkins_status
from .deploy_views import PublishView, DeployView, OperateView, HistoryView, deploy_cmd

app_name = 'deploy'

urlpatterns = [
    path('create/', login_required(DeployCreateView.as_view()),
         name='create'),
    path('list/', login_required(DeployListView.as_view()),
         name='list'),
    path('edit/<slug:pk>/', login_required(DeployUpdateView.as_view()),
         name='edit'),
    path('view/<slug:pk>/', login_required(DeployDetailView.as_view()),
         name='detail'),
    path('jenkins_build/', jenkins_build, name='jenkins_build'),
    path('jenkins_status/', jenkins_status, name='jenkins_status'),
]

urlpatterns += [
    path('publish/', login_required(PublishView.as_view()),
         name='publish'),
    path('deploy/<slug:app_name>/<slug:deploy_version>/<slug:env>/', login_required(DeployView.as_view()),
         name='deploy'),
    path(r'deploy-cmd/', deploy_cmd, name="deploy-cmd"),

    path('operate/', login_required(OperateView.as_view()),
         name='operate'),
    path('history/', login_required(HistoryView.as_view()),
             name='history'),
]

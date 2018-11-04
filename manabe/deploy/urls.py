from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import DeployCreateView, DeployUpdateView, DeployDetailView, DeployListView
from .views import jenkins_build, jenkins_status, update_deploypool_jenkins
from .deploy_views import PublishView, DeployView, OperateView, OperateAppView, HistoryView, deploy_cmd
from .upload_views import DeployVersionUploadView, fileupload

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
    path('update_deploypool_jenkins/', update_deploypool_jenkins,
         name='update_deploypool_jenkins'),
]

# upload
urlpatterns += [
    path('upload/', DeployVersionUploadView.as_view(),
         name='upload'),
    path('file_upload/', fileupload, name='file-upload'),
]

# deploy
urlpatterns += [
    path('publish/', login_required(PublishView.as_view()),
         name='publish'),
    path('deploy/<slug:app_name>/<slug:deploy_version>/<slug:env>/',
         login_required(DeployView.as_view()),
         name='deploy'),
    path(r'deploy-cmd/', deploy_cmd, name="deploy-cmd"),

    path('operate/', login_required(OperateView.as_view()),
         name='operate'),
    path('operate/<slug:app_name>/<slug:env>/',
         login_required(OperateAppView.as_view()),
         name='operate_app'),
    path('history/', login_required(HistoryView.as_view()),
             name='history'),
]

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import RightAdminView, admin_user, update_permission

app_name = 'rightadmin'

urlpatterns = [
    path('list/<slug:pk>/',
         login_required(RightAdminView.as_view()),
         name='list'),
    path('admin_user/<slug:app_id>/<slug:action_id>/<slug:env_id>/',
         login_required(admin_user),
             name='admin_user'),
    path('update_permission/',
         login_required(update_permission),
         name='update_permission'),
    path('default/',
         TemplateView.as_view(template_name="rightadmin/default.html"),
         name="default"),
]

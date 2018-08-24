from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import User
from appinput.models import App
from .models import Action, Permission
from envx.models import Env


class RightAdminView(TemplateView):
    template_name = 'rightadmin/list_rightadmin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_id = kwargs['pk']
        context['app'] = App.objects.get(id=app_id)
        context['action'] = Action.objects.all().order_by('aid')
        context['env'] = Env.objects.all()
        context['current_page'] = "rightadmin-list"
        context['current_page_name'] = "APP权限管理"
        return context


def admin_user(request, app_id, action_id, env_id):
    # 将所有用户区别为已有权限和没有权限(users, guests)，返回给前端页面作选择。
    all_user_set = User.objects.all().order_by("username")
    guests = []
    users = []
    filter_dict = dict()
    filter_dict['app_name__id'] = app_id
    filter_dict['action_name__id'] = action_id
    if env_id != '0':
        filter_dict['env_name__id'] = env_id
    try:
        permission_set = Permission.objects.get(**filter_dict)
        user_set = permission_set.main_user.all()
        for user in all_user_set:
            if user in user_set:
                users.append(user)
            else:
                guests.append(user)
    except Permission.DoesNotExist:
        guests = all_user_set
    return render(request, 'rightadmin/edit_user.html',
                  {'users': users,
                   'app_id': app_id,
                   'action_id': action_id,
                   'env_id': env_id,
                   'guests': guests})


def update_permission(request):
    pass
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import User
from appinput.models import App
from .models import Action, Permission
from envx.models import Env
from public.user_group import is_app_admin


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


@csrf_exempt
def update_permission(request):
    select_user = []
    app_id = 0
    action_id = 0
    env_id = 0
    # 获取并解析前台传过来的ajax参数
    group_data = request.POST.get('group_data')
    for item in group_data.split('&'):
        if item.startswith('selectUser'):
            select_user.append(item.split('=')[1])
        if item.startswith('app_id'):
            app_id = item.split('=')[1]
        if item.startswith('action_id'):
            action_id = item.split('=')[1]
        if item.startswith('env_id'):
            env_id = item.split('=')[1]
    if not is_app_admin(app_id, request.user):
        return JsonResponse({'return': 'error'})

    # 判断后来数据库是存已有相关记录，并进行更新。
    filter_dict = dict()
    filter_dict['app_name__id'] = app_id
    filter_dict['action_name__id'] = action_id
    if env_id != '0':
        filter_dict['env_name__id'] = env_id
    try:
        permission_item = Permission.objects.get(**filter_dict)
        new_users = User.objects.filter(id__in=select_user)
        permission_item.main_user.set(new_users)
        permission_item.save()
    except Permission.DoesNotExist:
        new_users = User.objects.filter(id__in=select_user)
        app = App.objects.get(id=app_id)
        action = Action.objects.get(id=action_id)

        name = '{}-{}-{}'.format(app_id, action_id, env_id)
        dic = {'name': name,
               'app_name': app,
               'action_name': action}
        if env_id != '0':
            env = Env.objects.get(id=env_id)
            dic['env_name'] = env

        permission_item = Permission.objects.create(**dic)
        permission_item.main_user.set(new_users)
        permission_item.save()

    return JsonResponse({'return': 'success'})

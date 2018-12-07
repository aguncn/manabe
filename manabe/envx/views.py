# coding=utf8
import time
from django.shortcuts import redirect
from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages

from deploy.models import DeployPool, DeployStatus, History
from .models import Env
from rightadmin.models import Action
from public.user_group import is_right, get_app_admin


class EnvXListView(ListView):
    template_name = 'envx/list_envx.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return DeployPool.objects.filter(
                Q(name__icontains=search_pk) | Q(description__icontains=search_pk)).exclude(
                deploy_status__name__in=["CREATE"]).order_by("-change_date")
        if self.request.GET.get('app_name'):
            app_name = self.request.GET.get('app_name')
            return DeployPool.objects.filter(app_name=app_name).exclude(
                deploy_status__name__in=["CREATE"]).order_by("-change_date")
        return DeployPool.objects.exclude(deploy_status__name__in=["CREATE"])\
            .order_by("-change_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "envx-list"
        context['current_page_name'] = "环境流转"
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class EnvXHistoryView(ListView):
    template_name = 'envx/list_history.html'
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return History.objects.filter(
                Q(name__icontains=search_pk) |
                Q(app_name__name__icontains=search_pk)).filter(do_type='XCHANGE')
        if self.request.GET.get('app_name'):
            app_name = self.request.GET.get('app_name')
            return History.objects.filter(app_name=app_name).filter(do_type='XCHANGE')
        return History.objects.filter(do_type='XCHANGE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "envx-history"
        context['current_page_name'] = "环境流转历史"
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


def change(request):
    if request.POST:
        if request.POST.get('deploy_id') is None or request.POST.get('env_id') is None:
            messages.error(request, '参数错误，请重新选择！', extra_tags='c-error')
            return redirect('envx:list')
        else:
            deploy_id = request.POST.get('deploy_id')
            env_id = request.POST.get('env_id')
            deploy_item = DeployPool.objects.get(id=deploy_id)
            org_env_name = deploy_item.env_name.name if deploy_item.env_name is not None else "BUILD"
            action_item = Action.objects.get(name="XCHANGE")
            app_id = deploy_item.app_name.id
            action_id = action_item.id
            if not is_right(app_id, action_id, 0, request.user):
                manage_user = get_app_admin(app_id)
                messages.error(request, '没有权限，请联系{}'.format(manage_user), extra_tags='c-error')
                return redirect('envx:list')
            env_name = Env.objects.get(id=env_id)
            deploy_status = DeployStatus.objects.get(name="READY")
            DeployPool.objects.filter(id=deploy_id).update(env_name=env_name, deploy_status=deploy_status)
            messages.success(request, '环境流转成功！', extra_tags='c-success')
            # 构建环境流转历史记录参数
            user = request.user;
            app_name = deploy_item.app_name
            content = {'before': org_env_name, 'after': env_name.name}
            add_history(user, app_name, deploy_item, content)
            return redirect('envx:list')
    else:
        return redirect('envx:list')


def add_history(user, app_name, deploy_name, content):
    History.objects.create(
        name=app_name.name + '-xchange-' + deploy_name.name + '-' + time.strftime("%Y-%m%d-%H%M%S", time.localtime()),
        user=user,
        app_name=app_name,
        deploy_name=deploy_name,
        do_type='XCHANGE',
        content=content
    )


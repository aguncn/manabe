# coding=utf8

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Q, F
from django.conf import settings
from .models import DeployPool, History
from serverinput.models import Server
from envx.models import Env
from appinput.models import App
from rightadmin.models import Action
from public.user_group import is_right, \
    get_app_admin, \
    is_admin_group

from .salt_cmd_views import deploy


class PublishView(ListView):
    template_name = 'deploy/publish.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return DeployPool.objects.filter(
                Q(name__icontains=search_pk) |
                Q(description__icontains=search_pk)).exclude(
                deploy_status__in=["CREATE", "BUILD"])
        if self.request.GET.get('app_name'):
            app_name = self.request.GET.get('app_name')
            return DeployPool.objects.filter(app_name=app_name).\
                exclude(deploy_status__name__in=["CREATE", "BUILD"])
        return DeployPool.objects.\
            exclude(deploy_status__name__in=["CREATE", "BUILD"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "deploy-list"
        context['current_page_name'] = "发布单列表"
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class DeployView(ListView):
    template_name = 'deploy/deploy.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        return Server.objects.filter(env_name__name=self.kwargs['env']).filter(
            app_name__name=self.kwargs['app_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = self.kwargs['app_name']
        deploy_version = self.kwargs['deploy_version']
        context['now'] = timezone.now()
        context['current_page'] = "deploy-list"
        context['current_page_name'] = "部署服务器列表"
        context['app_name'] = app_name
        context['deploy_version'] = deploy_version
        context['env'] = self.kwargs['env']
        deploy_item = DeployPool.objects.get(name=deploy_version)
        context['is_restart_status'] = deploy_item.app_name.is_restart_status
        context['deploy_type'] = deploy_item.deploy_type
        context['deploy_no'] = deploy_item.deploy_no
        context['is_inc_tot'] = deploy_item.is_inc_tot
        context['mablog_url'] = settings.MABLOG_URL

        # 用于权限判断及前端展示
        context['is_right'] = True
        app_id = deploy_item.app_name.id
        env_id = deploy_item.env_name.id
        action_item = Action.objects.get(name="DEPLOY")
        action_id = action_item.id
        if not is_right(app_id, action_id, env_id, self.request.user):
            context['is_right'] = False
            context['admin_user'] = get_app_admin(app_id)

        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class OperateView(ListView):
    template_name = 'deploy/operate.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return App.objects.filter(name__icontains=search_pk)
        if self.request.GET.get('app_name'):
            app_name = self.request.GET.get('app_name')
            return App.objects.filter(id=app_name)
        return App.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "operate-list"
        context['current_page_name'] = "组件列表"
        context['env_name'] = Env.objects.all()
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class OperateAppView(ListView):
    template_name = 'deploy/operate_app.html'
    paginate_by = 10

    def get_queryset(self):
        return Server.objects.filter(app_name=self.kwargs['app_name'], env_name=self.kwargs['env'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "operate-app"
        context['current_page_name'] = "服务器列表"

        app_item = App.objects.get(id=self.kwargs['app_name'])
        env_item = Env.objects.get(id=self.kwargs['env'])
        context['op_log_no'] = app_item.op_log_no
        context['app_name'] = app_item.name
        context['env'] = env_item.name
        context['mablog_url'] = settings.MABLOG_URL

        # 用于权限判断及前端展示
        context['is_right'] = True
        app_id = app_item.id
        env_id = env_item.id
        action_item = Action.objects.get(name="DEPLOY")
        action_id = action_item.id
        if not is_right(app_id, action_id, env_id, self.request.user):
            context['is_right'] = False
            context['admin_user'] = get_app_admin(app_id)

        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


@csrf_exempt
def deploy_cmd(request):
    user_name = request.user
    group_cmd = request.POST.get('group_cmd')
    print(group_cmd)
    is_restart_server = False
    subserver_list = []
    p_value = 0
    deploy_version = ''
    app_name = ''
    deploy_type = ''
    sp_type = ''
    operation_type = ''
    for cmd_data in group_cmd.split('&'):
        if cmd_data.startswith('serverSelect'):
            subserver_list.append(cmd_data.split('=')[1])
        if cmd_data.startswith('operation_type'):
            operation_type = cmd_data.split('=')[1]
        if cmd_data.startswith('deploy_version'):
            deploy_version = cmd_data.split('=')[1]
        if cmd_data.startswith('app_name'):
            app_name = cmd_data.split('=')[1]
        if cmd_data.startswith('deploy_type'):
            deploy_type = cmd_data.split('=')[1]
        if cmd_data.startswith('is-restart-server'):
            if cmd_data.split('=')[1] == 'restart':
                is_restart_server = True
        if cmd_data.startswith('sp_type'):
            sp_type = cmd_data.split('=')[1]
        if cmd_data.startswith('env'):
            env = cmd_data.split('=')[1]
        if cmd_data.startswith('p_value'):
            p_value = int(cmd_data.split('=')[1])

    # 串行等同于批次多于子服务器数量的并行，在列表分组时，使用了函数表达式
    if sp_type == "serial_deploy" or p_value > len(subserver_list):
        p_value = len(subserver_list)
    deploy_subserver_list = mod_group(subserver_list, p_value)
    # 为了后面的启停及锁定的代码及日志一致性，这里重置发布单变量
    deploy_version = deploy_version if deploy_version != '' else 'Demo'

    if deploy_version == "Demo":
        App.objects.filter(name=app_name).update(op_log_no=F('op_log_no') + 1)
        deploy_no = App.objects.get(name=app_name).op_log_no
    else:
        DeployPool.objects.filter(name=deploy_version).update(deploy_no=F('deploy_no') + 1)
        deploy_no = DeployPool.objects.get(name=deploy_version).deploy_no
    deploy(deploy_subserver_list, deploy_type, is_restart_server,
           user_name, deploy_version, operation_type)

    result = {'return': "OK"}
    return JsonResponse(result, status=200)


# 将传递过来的列表，按指定批次，返回分组列表
def mod_group(alist, agroup):
    tmp_list = [0] * agroup
    for i in range(len(alist)):
        m_value = i % agroup
        for j in range(agroup):
            if tmp_list[j] == 0:
                tmp_list[j] = []
            if m_value == j:
                tmp_list[j].append(alist[i])
    return tmp_list


class HistoryView(ListView):
    template_name = 'deploy/list_history.html'
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return History.objects.filter(
                Q(app_name__name__icontains=search_pk) |
                Q(content__icontains=search_pk))\
                .filter(do_type__in=["DEPLOY", "OPERATE"])
        if self.request.GET.get('app_name'):
            app_name = self.request.GET.get('app_name')
            return History.objects.filter(app_name__id=app_name)\
                .filter(do_type__in=["DEPLOY", "OPERATE"])
        return History.objects.filter(do_type__in=["DEPLOY", "OPERATE"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "deploy-history"
        context['current_page_name'] = "历史发布单列表"
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context

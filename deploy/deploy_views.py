# coding=utf8

from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Q
from .models import DeployPool
from serverinput.models import Server


class PublishView(ListView):
    template_name = 'deploy/publish.html'
    paginate_by = 4

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return DeployPool.objects.filter(Q(name__icontains=search_pk)|
                                      Q(script_template__icontains=search_pk)|
                                      Q(allow_user__username__icontains=search_pk))
        if self.request.GET.get('app_name') :
            app_name = self.kwargs['app_name']
            return DeployPool.objects.filter(id=app_name)
        return DeployPool.objects.all()

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
    paginate_by = 4

    def get_queryset(self, **kwargs):
        print(self.kwargs['env'], "###############")
        print(self.kwargs['app_name'], "@@@@@@@@@@@@")
        return Server.objects.filter(env_name__name=self.kwargs['env']).filter(
                app_name__name=self.kwargs['app_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "deploy-list"
        context['current_page_name'] = "部署服务器列表"
        context['app_name'] = self.kwargs['app_name']
        context['deploy_version'] = self.kwargs['deploy_version']
        context['env'] = self.kwargs['env']
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
    paginate_by = 4

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return DeployPool.objects.filter(Q(name__icontains=search_pk)|
                                      Q(script_template__icontains=search_pk)|
                                      Q(allow_user__username__icontains=search_pk))
        if self.request.GET.get('app_name') :
            app_name = self.kwargs['app_name']
            return DeployPool.objects.filter(id=app_name)
        return DeployPool.objects.all()

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
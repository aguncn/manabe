# coding=utf8
import random
import time
import string
import json
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import DeployForm
from .models import DeployPool
from rightadmin.models import Action
from django.conf import settings
from public.user_group import is_right


class DeployCreateView(CreateView):
    template_name = 'deploy/create_deploy.html'
    model = DeployPool
    form_class = DeployForm

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        user = self.request.user
        app = form.cleaned_data['app_name']
        action = Action.objects.get(name="CREATE")
        if not is_right(app.id, action.id, 0, user):
            messages.error(self.request, '没有权限，请联系此应用管理员:' + str(app.manage_user), extra_tags='c-error')
            return self.render_to_response({'form': form})
        random_letter = ''.join(random.sample(string.ascii_letters, 2))
        deploy_version = time.strftime("%Y-%m%d-%H%M%S", time.localtime()) + random_letter.upper()
        deploy = DeployPool.objects.create(
            name=deploy_version,
            description=form.cleaned_data['description'],
            app_name=app,
            branch_build=form.cleaned_data['branch_build'],
            is_inc_tot=form.cleaned_data['is_inc_tot'],
            deploy_type=form.cleaned_data['deploy_type'],
            deploy_status='CREATE',
            create_user=user,
        )
        deploy.save()
        return HttpResponseRedirect(reverse("deploy:list"))

    def get_success_url(self):
        return reverse_lazy("deploy:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "deploy-create"
        context['current_page_name'] = "新建发布单"
        return context


class DeployListView(ListView):
    template_name = 'deploy/list_deploy.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return DeployPool.objects.filter(Q(name__icontains=search_pk) | Q(description__icontains=search_pk)).filter(deploy_status__in=["CREATE"])
        if self.request.GET.get('app_name'):
            app_name = self.request.GET.get('app_name')
            return DeployPool.objects.filter(app_name=app_name).filter(deploy_status__in=["CREATE", "BUILD"])
        return DeployPool.objects.filter(deploy_status__in=["CREATE", "BUILD"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "deploy-list"
        context['current_page_name'] = "发布单列表"
        context['jenkins_url'] = settings.JENKINS_URL
        context['nginx_url'] = settings.NGINX_URL

        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class DeployDetailView(DetailView):
    template_name = 'deploy/detail_deploy.html'
    model = DeployPool

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = "发布单详情"
        context['now'] = timezone.now()
        return context


class DeployUpdateView(UpdateView):
    template_name = 'deploy/edit_deploy.html'
    model = DeployPool
    form_class = DeployForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "deploy-edit"
        context['current_page_name'] = "编辑发布单"
        context['app_id'] = self.kwargs.get(self.pk_url_kwarg, None)
        return context

    def get_success_url(self):
        return reverse_lazy("deploy:list")


@csrf_exempt
def jenkins_build(request):
    pass


def all_is_not_null(*args):
    for value in args:
        # print value
        if value == 'None' or len(value) == 0:
            return False
    return True


@csrf_exempt
def jenkins_status(request):
    pass


# coding=utf8
import random
import time
import string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import DeployForm
from .models import DeployPool


class DeployCreateView(CreateView):
    template_name = 'deploy/create_deploy.html'
    model = DeployPool
    form_class = DeployForm

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        current_user_set = self.request.user
        random_letter = ''.join(random.sample(string.ascii_letters, 2))
        deploy_version = time.strftime("%Y-%m%d-%H%M%S", time.localtime()) + random_letter.upper()
        deploy = DeployPool.objects.create(
            name=deploy_version,
            description=form.cleaned_data['description'],
            app_name=form.cleaned_data['app_name'],
            branch_build=form.cleaned_data['branch_build'],
            deploy_progress='CREATE',
            create_user=current_user_set,
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

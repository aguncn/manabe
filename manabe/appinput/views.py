# coding=utf8

from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import AppForm
from .models import App
from public.user_group import is_admin_group, is_right


class AppInputCreateView(CreateView):
    template_name = 'appinput/create_appinput.html'
    model = App
    form_class = AppForm

    def get(self, request, *args, **kwargs):
        # 定义用户权限
        if is_admin_group(self.request.user):
            return super().get(request, *args, **kwargs)
        else:
            result = "亲，没有权限，只有管理员才可进入！"
            return HttpResponse(result)

    def form_invalid(self, form):
        print(form)
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        App.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            jenkins_job=form.cleaned_data['jenkins_job'],
            git_url=form.cleaned_data['git_url'],
            build_cmd=form.cleaned_data['build_cmd'],
            package_name=form.cleaned_data['package_name'],
            zip_package_name=form.cleaned_data['zip_package_name'],
            is_restart_status=form.cleaned_data['is_restart_status'],
            script_url=form.cleaned_data['script_url'],
            manage_user=form.cleaned_data['manage_user'],
        )
        return HttpResponseRedirect(reverse("appinput:list"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "appinput-create"
        context['current_page_name'] = "新增APP应用"
        return context


class AppInputListView(ListView):
    template_name = 'appinput/list_appinput.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return App.objects.filter(
                Q(name__icontains=search_pk) |
                Q(package_name__icontains=search_pk))
        return App.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['is_admin_group'] = is_admin_group(self.request.user)
        context['current_page'] = "appinput-list"
        context['current_page_name'] = "APP应用列表"
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + "&".join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class AppInputDetailView(DetailView):
    template_name = 'appinput/detail_appinput.html'
    model = App

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = "APP应用详情"
        context['now'] = timezone.now()
        return context


class AppInputUpdateView(UpdateView):
    template_name = 'appinput/edit_appinput.html'
    model = App
    form_class = AppForm

    def get(self, request, *args, **kwargs):
        # 定义用户权限
        app_id = request.path.split("/")[-2]
        app_item = App.objects.get(id=app_id)
        if is_admin_group(self.request.user) \
                or app_item.manage_user == self.request.user:
            return super().get(request, *args, **kwargs)
        else:
            result = "亲，没有权限，只有管理员才可进入！"
            return HttpResponse(result)

    '''
    # 在提交时，限制非法用户权限
    def post(self, request, *args, **kwargs):
        app_id = request.path.split("/")[-2]
        app_item = App.objects.get(id=app_id)
        if is_admin_group(self.request.user) 
                or app_item.manage_user == self.request.user:
            return super().post(request, *args, **kwargs)
        else:
            result = "亲，没有权限，想用非正规方式修改吧？"
            return HttpResponse(result)
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "appinput-edit"
        context['current_page_name'] = "编辑APP应用"
        context['app_id'] = self.kwargs.get(self.pk_url_kwarg)
        return context

    def get_success_url(self):
        return reverse_lazy("appinput:list")

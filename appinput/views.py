# coding=utf8

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import AppForm
from .models import App


class AppInputCreateView(CreateView):
    template_name = 'appinput/create_appinput.html'
    model = App
    form_class = AppForm

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        current_user_set = self.request.user
        app = App.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            jenkins_job=form.cleaned_data['jenkins_job'],
            is_restart_status=form.cleaned_data['is_restart_status'],
            op_user=current_user_set,
        )
        app.save()
        return HttpResponseRedirect(reverse("appinput:appinput-list"))

    def get_success_url(self):
        return reverse_lazy("appinput:appinput-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = "appinput-create"
        context['current_page_name'] = "新增APP应用"
        return context


class AppInputListView(ListView):
    template_name = 'appinput/list_appinput.html'
    # model = App
    # queryset = App.objects.order_by('-change_date')
    paginate_by = 4

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return App.objects.filter(Q(name__icontains=search_pk)|
                                      Q(script_template__icontains=search_pk)|
                                      Q(allow_user__username__icontains=search_pk))
        if self.request.GET.get('app_name') :
            app_name = self.kwargs['app_name']
            return App.objects.filter(id=app_name)
        return App.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "appinput-edit"
        context['current_page_name'] = "编辑APP应用"
        context['app_id'] = self.kwargs.get(self.pk_url_kwarg, None)
        return context

    def get_success_url(self):
        return reverse_lazy("appinput:appinput-list")

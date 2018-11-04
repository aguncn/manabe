# coding=utf8
import random
import time
import string
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
import jenkins
from .forms import DeployForm
from .models import DeployPool, DeployStatus
from appinput.models import App
from rightadmin.models import Action
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
        DeployPool.objects.create(
            name=deploy_version,
            description=form.cleaned_data['description'],
            app_name=app,
            branch_build=form.cleaned_data['branch_build'],
            is_inc_tot=form.cleaned_data['is_inc_tot'],
            deploy_type=form.cleaned_data['deploy_type'],
            deploy_status=DeployStatus.objects.get(name='CREATE'),
            create_user=user,
        )
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
            return DeployPool.objects.filter(Q(name__icontains=search_pk) | Q(description__icontains=search_pk)).filter(
                deploy_status__name__in=["CREATE"])
        if self.request.GET.get('app_name'):
            app_name = self.request.GET.get('app_name')
            return DeployPool.objects.filter(app_name=app_name).filter(deploy_status__name__in=["CREATE", "BUILD"])
        return DeployPool.objects.filter(deploy_status__name__in=["CREATE", "BUILD"])

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


# 使用python-jenkins第三方库来提交jenkins任务
@csrf_exempt
def jenkins_build(request):
    # 获取前端ajax参数
    app_name = request.POST.get('app_name')
    deploy_version = request.POST.get('deploy_version')
    jenkins_job = request.POST.get('jenkins_job')
    deploy_version_set = DeployPool.objects.get(name=deploy_version)
    branch_build = deploy_version_set.branch_build
    app_set = App.objects.get(name=app_name)
    git_url = app_set.git_url
    package_name = app_set.package_name
    dir_build_file = app_set.dir_build_file
    zip_package_name = app_set.zip_package_name
    build_cmd = app_set.build_cmd

    # 构造jenkins job的字典参数，这些参数在jenkins里是字符型参数
    jenkins_dict = {
        'git_url': git_url,
        'branch_build': branch_build,
        'package_name': package_name,
        'app_name': app_name,
        'deploy_version': deploy_version,
        'dir_build_file': dir_build_file,
        'zip_package_name': zip_package_name,
        'build_cmd': build_cmd
    }

    if all_is_not_null([jenkins_job, app_name, branch_build, deploy_version]):
        # 按python-jenkins的API要求，生成jenkins服务器实例，并传递参数给build_job
        jenkins_url = settings.JENKINS_URL
        jenkins_username = settings.JENKINS_USERNAME
        jenkins_password = settings.JENKINS_PASSWORD
        server = jenkins.Jenkins(url=jenkins_url,
                                 username=jenkins_username,
                                 password=jenkins_password)
        next_build_number = server.get_job_info(jenkins_job)['nextBuildNumber']
        try:
            server.build_job(jenkins_job, jenkins_dict)
            from time import sleep
            sleep(10)
            result = {"return": "success", "build_number": next_build_number}
            status_code = 201
        except Exception as e:
            print(e)
            result = {"return": "error", "build_number": next_build_number}
            status_code = 501
        return JsonResponse(result, status=status_code)

    else:
        result = {"return": "error"}
        return JsonResponse(result, status=501)


def all_is_not_null(*args):
    for value in args:
        if value == 'None' or len(value) == 0:
            return False
    return True


# 前端通过ajax实时获取jenkins的编译任务的进度
@csrf_exempt
def jenkins_status(request):
    jenkins_job = request.POST.get('jenkins_job')
    next_build_number = int(request.POST.get('next_build_number'))
    jenkins_url = settings.JENKINS_URL
    jenkins_username = settings.JENKINS_USERNAME
    jenkins_password = settings.JENKINS_PASSWORD
    server = jenkins.Jenkins(url=jenkins_url,
                             username=jenkins_username,
                             password=jenkins_password)
    # 通过get_build_info方法，可以获取编译状态及结果状态
    building_info = server.get_build_info(jenkins_job, next_build_number)["building"]
    built_result = server.get_build_info(jenkins_job, next_build_number)["result"]
    result = {"return": "building",
              "building_info": building_info,
              "built_result": built_result}
    if built_result == 'SUCCESS':
        git_seg = server.get_build_info(jenkins_job, next_build_number)["actions"][5]
        git_version = git_seg['lastBuiltRevision']['SHA1']
        result["git_version"] = git_version
    return JsonResponse(result, status=200)


# 接受前台数据，更新发布单
@csrf_exempt
def update_deploypool_jenkins(request):
    current_user = request.user
    app_name = request.POST.get('app_name')
    deploy_version = request.POST.get('deploy_version')
    next_build_number = request.POST.get('next_build_number')
    git_version = request.POST.get('git_version')
    # 按nginx服务器地址，app应用，发布单号的目录层次构建软件包目录
    nginx_base_url = settings.NGINX_URL
    nginx_url = "{}/{}/{}".format(nginx_base_url, app_name, deploy_version)
    try:
        DeployPool.objects.filter(name=deploy_version).update(
            jenkins_number=str(next_build_number),
            code_number=git_version,
            nginx_url=nginx_url,
            deploy_status=DeployStatus.objects.get(name='BUILD'),
            create_user=current_user
        )
        result = {"return": "success", "build_number": next_build_number}
        status_code = 201
    except Exception as e:
        print(e)
        result = {"return": "error", "build_number": next_build_number}
        status_code = 501
    return JsonResponse(result, status=status_code)


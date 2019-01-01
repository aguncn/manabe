# coding:utf8
# 首先导入系统库，再导入框架库，最后导入用户库
import platform
import django
from django.views.generic.base import TemplateView
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from appinput.models import App
from serverinput.models import Server
from deploy.models import DeployPool
from rest_framework.authtoken.models import Token

from .forms import LoginForm, RegisterForm


class IndexView(TemplateView):
    template_name = "manabe/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "index"
        context['app_count'] = App.objects.count()
        context['server_count'] = Server.objects.count()
        context['deploy_count'] = DeployPool.objects.count()
        context['REMOTE_ADDR'] = self.request.META.get("REMOTE_ADDR")
        context['HTTP_USER_AGENT'] = self.request.META.get("HTTP_USER_AGENT")
        context['HTTP_ACCEPT_LANGUAGE'] = self.request.META.get("HTTP_ACCEPT_LANGUAGE")
        context['platform'] = platform.platform()
        context['python_version'] = platform.python_version()
        context['django_version'] = django.get_version()

        return context


def redirect_login(request):
    login_url = reverse('index')
    return HttpResponseRedirect(request.POST.get('next', login_url) or login_url)


@require_http_methods(["GET", "POST"])
def user_login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        vc = request.POST['vc']
        if vc.upper() != request.session['verify_code']:
            error.append('验证码错误！')
            return render(request, "accounts/login.html", locals())
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect_login(request)
            else:
                error.append('请输入正确的用户名和密码')
                return render(request, "accounts/login.html", locals())
        else:
            return render(request, "accounts/login.html", locals())
    else:
        form = LoginForm()
        return render(request, "accounts/login.html", locals())


@require_http_methods(["GET", "POST"])
def user_register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password2 = data['password2']
            if not User.objects.all().filter(username__iexact=username):
                if form.pwd_validate(password, password2):
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email)
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect_login(request)
                else:

                    error.append('密码不一致，请确认')
                    return render(request, 'accounts/register.html', locals())
            else:
                error.append('已存在相同用户名，请更换用户名')
                return render(request, 'accounts/register.html', locals())
        else:
                error.append('请确认各个输入框无误')
                return render(request, 'accounts/register.html', locals())
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', locals())


def gettoken(request):
    if request.method == 'GET':
        token_key = dict()
        token_key["username"] = request.user.username
        token_key["token"] = Token.objects.get(user=request.user).key
        return JsonResponse(token_key)



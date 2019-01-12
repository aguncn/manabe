import os
import hashlib
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .forms import ChangepwdForm, ChangeEmailForm, PwdResetForm


@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == 'GET':
        form = ChangepwdForm()
        return render(request, 'accounts/change_password.html', {'form': form, 'current_page_name': '更改密码'})
    else:
        error = []
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword1 = request.POST.get('newpassword1', '')
                user.set_password(newpassword1)
                user.save()
                return render(request, 'accounts/change_password.html', {'changepwd_success': True, })
            else:
                error.append('原密码输入错误，请重新输入')
                return render(request, 'accounts/change_password.html', locals())
        else:
            error.append('两次新密码不匹配，请重新输入')
            return render(request, 'accounts/change_password.html', locals())


def change_token(request):
    if request.method == 'POST':
        token_key = hashlib.sha1(os.urandom(24)).hexdigest()
        Token.objects.filter(user_id=request.user.id).update(key=token_key)
        context_dict = {
            'token_str': token_key
        }
        return render(request, 'accounts/change_token.html', context_dict)
    else:

        # 获取已有的token
        context_dict = {
            'token_str': Token.objects.get(user=request.user).key,
            'current_page_name': "Token管理"
        }
        return render(request, 'accounts/change_token.html', context_dict)


@require_http_methods(["GET", "POST"])
def change_email(request):
    if request.method == 'GET':
        form = ChangeEmailForm()
        return render(request, 'accounts/change_email.html',
                      {'form': form,
                       'current_page_name': '更改邮箱',
                       'email': User.objects.get(username=request.user.username).email,
                       })
    else:
        error = []
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            username = request.user.username
            new_email1 = request.POST.get('new_email1')
            User.objects.filter(username=request.user.username).update(email=new_email1)
            email = User.objects.get(username=request.user.username).email
            change_email_success = True
            return render(request, 'accounts/change_email.html', locals())
        else:
            error.append('两次新邮箱不匹配，或是邮箱格式错误，请重新输入')
            email = User.objects.get(username=request.user.username).email
            return render(request, 'accounts/change_email.html', locals())

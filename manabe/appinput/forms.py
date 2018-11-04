# coding:utf-8

from django.contrib.auth.models import User
from django import forms
from .models import App


class AppForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        required=True,
        error_messages={'required': "不能为空"},
        label=u"APP组件名称",
        widget=forms.TextInput(
            attrs={
                'placeholder': "名称",
                'class': 'input-text',
            }
        ),
    )
    description = forms.CharField(
        required=False,
        label=u"描述",
        widget=forms.Textarea(
            attrs={
                'placeholder': "描述",
                'class': 'input-text',
            }
        ),
    )
    jenkins_job = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"JENKINS JOB名称",
        widget=forms.TextInput(
            attrs={
                'placeholder': "Jenkins Job",
                'class': 'input-text',
            }
        ),
    )
    git_url = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"GIT地址",
        widget=forms.TextInput(
            attrs={
                'placeholder': "GIT地址",
                'class': 'input-text',
            }
        ),
    )
    dir_build_file = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"编译目录",
        widget=forms.TextInput(
            attrs={
                'placeholder': "./",
                'class': 'input-text',
            }
        ),
    )
    build_cmd = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"编译命令",
        widget=forms.TextInput(
            attrs={
                'placeholder': "编译命令",
                'class': 'input-text',
            }
        ),
    )
    package_name = forms.CharField(
        label=u"软件包名称",
        widget=forms.TextInput(
            attrs={
                'placeholder': "编译后的软件包名称，没有可不填",
                'class': 'input-text',
            }
        ),
    )
    zip_package_name = forms.CharField(
        label=u"压缩包名称",
        widget=forms.TextInput(
            attrs={
                'placeholder': "软件包和配置文件集成的压缩包，没有可不填",
                'class': 'input-text',
            }
        ),
    )
    is_restart_status = forms.CharField(
        error_messages={'required': "不能为空"},
        required=False,
        label=u"重启服务",
        widget=forms.CheckboxInput(
            attrs={
                'class': 'radio-box',
            }
        ),
    )
    manage_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=u"管理员",
        widget=forms.Select(
            attrs={
                'style': """width:40%;""",
                'class': 'select-box',
            }
        ),
    )

    script_url = forms.CharField(
        label=u"app脚本链接",
        widget=forms.TextInput(
            attrs={
                'placeholder': "http://[nginx]/scripts/[app_name]/[script_name]",
                'class': 'input-text',
            }
        ),
    )

    class Meta:
        model = App
        exclude = ['op_log_no']

# coding:utf-8

from django import forms
from .models import Server
from appinput.models import App
from envx.models import Env


class ServerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"服务器名称",
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
    ip_address = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"IP",
        widget=forms.TextInput(
            attrs={
                'placeholder': "ip_address",
                'class': 'input-text',
            }
        ),
    )
    port = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"port",
        widget=forms.TextInput(
            attrs={
                'placeholder': "port",
                'class': 'input-text',
            }
        ),
    )
    salt_name = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"salt_name",
        widget=forms.TextInput(
            attrs={
                'placeholder': "salt_name",
                'class': 'input-text',
            }
        ),
    )
    app_name = forms.ModelChoiceField(
        required=True,
        queryset=App.objects.all(),
        label=u"App",
        widget=forms.Select(
            attrs={
                'style': """width:40%;""",
                'class': 'select-box',
            }
        ),
    )

    env_name = forms.ModelChoiceField(
        required=True,
        queryset=Env.objects.all(),
        label=u"所属环境",
        widget=forms.Select(
            attrs={
                'style': """width:40%;""",
                'class': 'select-box',
            }
        ),
    )

    ip_address = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"IP",
        widget=forms.TextInput(
            attrs={
                'placeholder': "ip_address",
                'class': 'input-text',
            }
        ),
    )

    app_user = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"启动用户",
        widget=forms.TextInput(
            attrs={
                'placeholder': "root",
                'class': 'input-text',
            }
        ),
    )

    class Meta:
        model = Server
        # exclude = ['app_args', 'op_user']
        fields = ('name', 'description',
                  'ip_address', 'port',
                  'salt_name', 'app_name',
                  'env_name', 'app_user', 'op_user')


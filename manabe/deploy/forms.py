# coding:utf-8

from django import forms
from .models import DeployPool
from appinput.models import App

IS_INC_TOT_CHOICES = (
    ('TOT', r'全量部署'),
    ('INC', r'增量部署'),
)

DEPLOY_TYPE_CHOICES = (
    ('deployall', r'发布所有'),
    ('deploypkg', r'发布程序'),
    ('deploycfg', r'发布配置'),
)


class DeployForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        required=False,
        error_messages={'required': "不能为空"},
        label=u"发布单名称",
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
    branch_build = forms.CharField(
        required=True,
        label=u"Git 版本",
        widget=forms.TextInput(
            attrs={
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
    is_inc_tot = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"部署方式",
        widget=forms.Select(
            choices=IS_INC_TOT_CHOICES,
            attrs={
                'class': 'select-box',
            }
        ),
    )

    deploy_type = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"程序配置",
        widget=forms.Select(
            choices=DEPLOY_TYPE_CHOICES,
            attrs={
                'class': 'select-box',
            }
        ),
    )

    class Meta:
        model = DeployPool
        # exclude = ['app_args', 'op_user']
        fields = ('name', 'description', 'app_name', 'branch_build', 'is_inc_tot', 'deploy_type')


class UploadFileForm(forms.Form):
    name = forms.CharField(
        required=False,
        error_messages={'required': "不能为空"},
        label=u"发布单名称",
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
    is_inc_tot = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"部署方式",
        widget=forms.Select(
            choices=IS_INC_TOT_CHOICES,
            attrs={
                'class': 'form-control col-md-2',
            }
        ),
    )
    deploy_type = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"程序配置",
        widget=forms.Select(
            choices=DEPLOY_TYPE_CHOICES,
            attrs={
                'class': 'form-control col-md-2',
            }
        ),
    )
    is_inc_tot = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"部署方式",
        widget=forms.Select(
            choices=IS_INC_TOT_CHOICES,
            attrs={
                'class': 'select-box',
            }
        ),
    )
    deploy_type = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"程序配置",
        widget=forms.Select(
            choices=DEPLOY_TYPE_CHOICES,
            attrs={
                'class': 'select-box',
            }
        ),
    )
    file_path = forms.CharField(
        required=True,
        label=u"上传文件",
        widget=forms.TextInput(
            attrs={
                'rows': 2,
                'placeholder': "上传后自动生成",
            }
        ),
    )

    class Meta:
        model = DeployPool
        # exclude = ['app_args', 'op_user']
        fields = ('name', 'description', 'app_name', 'branch_build', 'is_inc_tot', 'deploy_type')





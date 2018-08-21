# coding:utf-8

from django import forms
from .models import App


class AppForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
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
    package_name = forms.CharField(
        error_messages={'required': "不能为空"},
        label=u"软件包名称",
        widget=forms.TextInput(
            attrs={
                'placeholder': "Package Name",
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

    script = forms.CharField(
        required=True,
        label=u"APP脚本",
        widget=forms.Textarea(
            attrs={
                'rows': 15,
                'style': """width:75%;""",
                'class': 'textarea',
            }
        ),
    )

    class Meta:
        model = App
        exclude = ['op_user']


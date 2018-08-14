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

    class Meta:
        model = App
        exclude = ['app_args', 'op_user']


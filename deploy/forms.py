# coding:utf-8

from django import forms
from .models import DeployPool
from appinput.models import App


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

    class Meta:
        model = DeployPool
        # exclude = ['app_args', 'op_user']
        fields = ('name', 'description', 'app_name', 'branch_build')


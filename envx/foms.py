
from django import forms
from .models import Env


class EnvForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        required=True,
        error_messages={'required': "不能为空"},
        label=u"环境名称",
        widget=forms.TextInput(
            attrs={
                'placeholder': "环境",
                'class': 'input-text',
            }
        ),
    )

    class Meta:
        model = Env
        fields = ['name']
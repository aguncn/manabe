# coding:utf8
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"帐号",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"帐号",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label=u"邮箱",
        error_messages={'required': u'请输入电子邮箱'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"此邮箱用于密码找回",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ))
    password2 = forms.CharField(
        required=True,
        error_messages={'required': u'请再次输入密码'},
        label='Confirm',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ))

    def pwd_validate(self, p1, p2):
        return p1 == p2


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"原密码",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"新密码",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )

    def clean(self):
        print(self.cleaned_data, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            print("*****************************")
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class ChangeEmailForm(forms.Form):
    new_email1 = forms.EmailField(
        required=True,
        label=u"新邮箱地址",
        error_messages={'required': u'请输入新邮箱地址'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"新邮箱地址",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )
    new_email2 = forms.EmailField(
        required=True,
        label=u"新邮箱地址",
        error_messages={'required': u'请再次输入新邮箱地址'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"确认新邮箱地址",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )

    def clean(self):
        print(self.cleaned_data, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['new_email1'] != self.cleaned_data['new_email2']:
            print("*****************************")
            raise forms.ValidationError(u"两次输入的邮箱地址不一样")
        else:
            cleaned_data = super(ChangeEmailForm, self).clean()
        return cleaned_data


class PwdResetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=u"邮箱",
        error_messages={'required': u'请输入注册时的电子邮箱'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"请输入注册时的电子邮箱",
                'rows': 1,
                'class': 'input-text size-L',
            }
        ),
    )
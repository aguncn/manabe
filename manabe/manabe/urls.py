"""manabe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import IndexView, user_login, user_register
from public.verifycode import verify_code
from .password_views import change_token, change_email
from .password_views import change_password
from django.contrib.auth.views import logout_then_login
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(IndexView.as_view()), name="index"),
    path('accounts/register/', user_register, name='register'),
    path('accounts/login/', user_login, name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('verify_code/', verify_code, name='verify_code'),
    path('donation/', TemplateView.as_view(template_name="manabe/donation.html"), name="donation"),

]

urlpatterns += [
    path('change_token/',
         login_required(change_token),
         name="change_token"),
    path('accounts/change_email/',
         login_required(change_email),
         name="change_email"),
    path('accounts/change_password/',
         login_required(change_password),
         name="change_password"),
    path('reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]

urlpatterns += [
    path('public/', include('public.urls')),
]

urlpatterns += [
    path('app/', include('appinput.urls')),
]

urlpatterns += [
    path('server/', include('serverinput.urls')),
]

urlpatterns += [
    path('deploy/', include('deploy.urls')),
]

urlpatterns += [
    path('envx/', include('envx.urls')),
]

urlpatterns += [
    path('rightadmin/', include('rightadmin.urls')),
]

# RESTful api
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),
    path('api/', include('api.urls')),
]
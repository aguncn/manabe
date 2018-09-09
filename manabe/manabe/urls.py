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
from .views import IndexView, user_login, user_register, change_password
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(IndexView.as_view()), name="index"),
    path('accounts/register/', user_register, name='register'),
    path('accounts/login/', user_login, name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('donation/', TemplateView.as_view(template_name="manabe/donation.html"), name="donation"),
    path('accounts/change-password/', login_required(change_password), name="change-password"),
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
#coding:utf-8
# Create your views here.

from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import time
import random
import string
import platform
import json
import shutil
import errno
from django.conf import settings
from .forms import UploadFileForm
from .models import DeployPool, DeployStatus


def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


class DeployVersionUploadView(FormView):
    template_name = 'deploy/upload_deployversion.html'
    form_class = UploadFileForm

    def form_invalid(self, form):
        return self.render_to_response(RequestContext(self.request, {'form': form}))

    def form_valid(self, form):

        current_user = self.request.user
        random_letter = ''.join(random.sample(string.ascii_letters, 2))
        deploy_version = time.strftime("%Y-%m%d-%H%M%S", time.localtime()) + random_letter.upper()
        description = form.cleaned_data['description']
        app_name = form.cleaned_data['app_name']
        is_inc_tot = form.cleaned_data['is_inc_tot']
        deploy_type = form.cleaned_data['deploy_type']
        file_path = form.cleaned_data['file_path']

        deployversion_upload_done(app_name, deploy_version, file_path)
        nginx_base_url = settings.NGINX_URL
        nginx_url = "{}/{}/{}".format(nginx_base_url, app_name, deploy_version)

        DeployPool.objects.create(
            name=deploy_version,
            app_name=app_name,
            branch_build="upload",
            is_inc_tot=is_inc_tot,
            deploy_type=deploy_type,
            create_user=current_user,
            nginx_url=nginx_url,
            description=description,
            deploy_status=DeployStatus.objects.get(name='BUILD'),
        )
        return HttpResponseRedirect(reverse("deploy:list"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = "新建发布单(上传)"
        return context

    def get_success_url(self):
        return reverse_lazy("version:deployversion-list")


@csrf_exempt
def fileupload(request):
    files = request.FILES.getlist('files[]')
    file_name_list = []
    for f in files:
        if platform.system() == "Windows":
            destination = 'd://tmp//'
        elif platform.system() == "Linux":
            destination = "/tmp/"  # linux
        else:
            destination = "/tmp/"  # linux
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open(destination+f.name, 'wb+') as destination:
            for chunk in f.chunks(chunk_size=10000):
                destination.write(chunk)
        file_name_list.append(f.name)
    return render_to_json_response(','.join(file_name_list))


def deployversion_upload_done(app_name, deploy_version, upload_file):
        if platform.system() == "Windows":
            src_file = 'd://tmp//' + upload_file
            dest_folder = 'd://nfsc//'
        elif platform.system() == "Linux":
            src_file = "/tmp/" + upload_file
            dest_folder = "/nfsc/{}/{}/".format(app_name, deploy_version)

        mkdir_p(dest_folder)
        dest_file = dest_folder + upload_file
        shutil.move(src_file, dest_file)
        # :param site_name:
        # :param app_name:
        # :param deploy_version:
        # :param upload_file:
        # :return:
        # post_prismfilesave(app=app_name, file_name=upload_file, dep_version=deploy_version)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise OSError

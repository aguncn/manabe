from django.views.generic import TemplateView
from django.http import HttpResponse
from appinput.models import App
from rightadmin.models import Action
from envx.models import Env


class RightAdminView(TemplateView):
    template_name = 'rightadmin/list_rightadmin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_id = kwargs['pk']
        context['app'] = App.objects.get(id=app_id)
        context['action'] = Action.objects.all().order_by('aid')
        context['env'] = Env.objects.all()
        context['current_page'] = "rightadmin-list"
        context['current_page_name'] = "APP权限管理"
        return context


def admin_user(request, app_id, action_id, env_id):
    print(app_id, action_id, env_id, "@@@@@@@@@@@@@@@@")
    return HttpResponse("hello")

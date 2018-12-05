from datetime import datetime, timedelta
from django.http import JsonResponse
from  django.views.generic.base  import TemplateView
from deploy.models import DeployPool
from envx.models import Env
from django.db.models import Count


def get_deploy_count(request):
    return_list = []
    now = datetime.now()
    a_month = now - timedelta(days=60)
    select = {'day': 'date(add_date)'}
    env = request.GET.get('env', 'All')
    if env != 'All':
        env_id = Env.objects.get(name=env).id
        a_month_deploy_qs = DeployPool.objects. \
            filter(env_name_id=env_id). \
            filter(add_date__range=(a_month, now)). \
            extra(select=select).\
            values('day').\
            distinct().\
            order_by("day").\
            annotate(number=Count('add_date'))
    else:
        a_month_deploy_qs = DeployPool.objects. \
            filter(add_date__range=(a_month, now)). \
            extra(select=select). \
            values('day'). \
            distinct(). \
            order_by("day"). \
            annotate(number=Count('add_date'))
    for item in a_month_deploy_qs:
        item_dict = {}
        item_key = item['day'].strftime('%m-%d')
        item_dict[item_key] = item['number']
        return_list.append(item_dict)

    return JsonResponse(return_list, safe=False)


def get_app_deploy_count(request):
    return_list = []
    app_deploy_qs = DeployPool.objects.\
        values('app_name__name'). \
        distinct(). \
        annotate(number=Count('app_name')).order_by('-number')[:10]
    for item in app_deploy_qs:
        item_dict = {}
        item_key = item['app_name__name']
        item_dict[item_key] = item['number']
        return_list.append(item_dict)
    return JsonResponse(return_list, safe=False)


class DeployCountView(TemplateView):
    template_name = "deploy/deploy_count.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = "发布数据"
        return context


class AppDeployCountView(TemplateView):
    template_name = "deploy/app_deploy_count.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = "应用统计"
        return context




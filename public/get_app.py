from django.http import JsonResponse
from appinput.models import App


def get_app(request):
    app_dict = {}
    app_set = App.objects.all()
    for item in app_set:
        app_dict[item.id] = item.name
    return JsonResponse(app_dict)

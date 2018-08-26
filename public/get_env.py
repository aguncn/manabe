from django.http import JsonResponse
from envx.models import Env


def get_env(request):
    env_dict = {}
    env_set = Env.objects.all()
    for item in env_set:
        env_dict[item.id] = item.name
    return JsonResponse(env_dict)

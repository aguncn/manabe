from random import sample, choice
from django.contrib.auth.models import User
from rightadmin.models import Action, Permission
from appinput.models import App
from envx.models import Env


def fake_permission_data():
    Permission.objects.all().delete()
    print('delete all permission data')
    user_set = User.objects.all()
    app_set = App.objects.all()
    env_set = Env.objects.all()
    action_set = Action.objects.all()
    for action_item in action_set:
        if action_item.name in ['CREATE', 'XCHANGE']:
            for app_item in app_set:
                name = '{}-{}'.format(app_item.id, action_item.id)
                pm = Permission.objects.create(name=name,
                                               app_name=app_item,
                                               env_name=None,
                                               action_name=action_item)
                pm.main_user.set(sample(list(user_set), 5))
                pm.save()
        else:
            for app_item in app_set:
                env = choice(env_set)
                name = '{}-{}-{}'.format(app_item.id, action_item.id, env.id)
                pm = Permission.objects.create(name=name,
                                               app_name=app_item,
                                               env_name=env,
                                               action_name=action_item)
                pm.main_user.set(sample(list(user_set), 5))
                pm.save()
    print('create action permission data')

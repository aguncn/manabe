from random import choice
from django.contrib.auth.models import User
from appinput.models import App
from envx.models import Env
from serverinput.models import Server


def fake_server_data():
    Server.objects.all().delete()
    print('delete all server data')

    user_set = User.objects.all()
    app_set = App.objects.all()
    env_set = Env.objects.all()
    for i in range(100):
        ip_address = salt_name = "192.168.0.{}".format(i)
        for j in [80, 443, 8080, 8888]:
            port = j
            name = "192.168.0.{}_{}".format(i, port)
            app_user = choice(['root', 'tomcat', 'javauser'])
            op_user = choice(user_set)
            app_item = choice(app_set)
            env_item = choice(env_set)

            Server.objects.create(name=name, ip_address=ip_address, port=port,
                                  salt_name=salt_name, env_name=env_item,
                                  app_name=app_item, op_user=op_user,
                                  app_user=app_user)
    print('create all server data')

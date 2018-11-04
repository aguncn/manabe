import random
import time
import string
from random import choice
from django.contrib.auth.models import User
from appinput.models import App
from envx.models import Env
from deploy.models import DeployPool, DeployStatus


def fake_deploy_data():
    DeployPool.objects.all().delete()
    print('delete all deploy  data')

    app_set = App.objects.all()
    env_set = Env.objects.all()
    user_set = User.objects.all()
    is_inc_tot = ['TOT', 'INC']
    deploy_type = ['deployall', 'deploypkg', 'deploycfg']
    deploy_status_set_env = DeployStatus.objects.\
        filter(name__in=['READY', 'ING', 'FINISH', 'ERROR'])
    deploy_status_set_create = DeployStatus.objects.get(name='CREATE')
    deploy_status_set_build = DeployStatus.objects.get(name='BUILD')

    for date_no in range(30):
        random_letter = ''.join(random.sample(string.ascii_letters, 2))
        time_str = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
        fake_time_str = time_str.split("-")
        fake_time_str[2] = str(date_no)
        fake_time_str = '-'.join(fake_time_str)
        name = fake_time_str + random_letter.upper()
        DeployPool.objects.create(name=name, description="test",
                                  branch_build="master",
                                  jenkins_number=date_no,
                                  code_number=date_no+10,
                                  is_inc_tot=choice(is_inc_tot),
                                  deploy_type=choice(deploy_type),
                                  create_user=choice(user_set),
                                  app_name=choice(app_set),
                                  env_name=choice(env_set),
                                  deploy_status=choice(deploy_status_set_env),
                                  nginx_url="http://localhost/"
                                  )
    for date_no in range(30):
        random_letter = ''.join(random.sample(string.ascii_letters, 2))
        time_str = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
        fake_time_str = time_str.split("-")
        fake_time_str[2] = str(date_no)
        fake_time_str = '-'.join(fake_time_str)
        name = fake_time_str + random_letter.upper()
        if date_no % 2 == 1:
            DeployPool.objects.create(name=name,
                                      description="test",
                                      branch_build="master",
                                      jenkins_number=date_no,
                                      code_number=date_no+10,
                                      is_inc_tot=choice(is_inc_tot),
                                      deploy_type=choice(deploy_type),
                                      create_user=choice(user_set),
                                      app_name=choice(app_set),
                                      deploy_status=deploy_status_set_create,
                                      )
        else:
            DeployPool.objects.create(name=name,
                                      description="test",
                                      branch_build="master",
                                      jenkins_number=date_no,
                                      code_number=date_no + 10,
                                      is_inc_tot=choice(is_inc_tot),
                                      deploy_type=choice(deploy_type),
                                      create_user=choice(user_set),
                                      app_name=choice(app_set),
                                      deploy_status=deploy_status_set_build,
                                      nginx_url="http://localhost/"
                                      )
    print('create all deploy data')

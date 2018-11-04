from random import choice
from django.contrib.auth.models import User
from appinput.models import App


def fake_app_data():
    App.objects.all().delete()
    print('delete all app data')
    user_set = User.objects.all()
    app_list = ['ABC-FRONT-APP-ADMIN',
                'ABC-FRONT-APP-NGINX',
                'ABC-FRONT-APP-VUEJS',
                'ABC-FRONT-APP-ANGULAR',
                'ABC-FRONT-APP-BOOTSTRAP',
                'ABC-BACKEND-NODEJS',
                'ABC-BACKEND-JAVA',
                'ABC-BACKEND-GO',
                'ABC-BACKEND-PYTHON',
                'ABC-BACKEND-SCALA',
                'ZEP-FRONT-APP-ADMIN',
                'ZEP-FRONT-APP-NGINX',
                'ZEP-FRONT-APP-VUEJS',
                'ZEP-FRONT-APP-ANGULAR',
                'ZEP-FRONT-APP-BOOTSTRAP',
                'ZEP-BACKEND-NODEJS',
                'ZEP-BACKEND-JAVA',
                'ZEP-BACKEND-GO',
                'ZEP-BACKEND-PYTHON',
                'ZEP-BACKEND-SCALA',
    ]

    for app_item in app_list:
        App.objects.create(name=app_item, jenkins_job=app_item,
                           git_url="http://localhost",
                           build_cmd="mvn package",
                           package_name=app_item+'.zip',
                           manage_user=choice(user_set))

    print('create all app data')

from rightadmin.models import Action


def fake_action_data():
    Action.objects.all().delete()
    print('delete all action data')
    Action.objects.create(name="CREATE", description='创建及编译', aid=1)
    Action.objects.create(name="XCHANGE", description='环境流转', aid=2)
    Action.objects.create(name="DEPLOY", description='部署', aid=3)
    print('create action action data')

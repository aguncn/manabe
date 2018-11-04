from deploy.models import DeployStatus


def fake_deploy_status_data():
    DeployStatus.objects.all().delete()
    print('delete all deploy status data')
    DeployStatus.objects.create(name="CREATE",
                                description="新建",
                                memo="新建")
    DeployStatus.objects.create(name="BUILD",
                                description="编译",
                                memo="新建")
    DeployStatus.objects.create(name="READY",
                                description="准备发布",
                                memo="准备发布")
    DeployStatus.objects.create(name="ING",
                                description="发布中...",
                                memo="发布中...")
    DeployStatus.objects.create(name="FINISH",
                                description="发布完成",
                                memo="发布完成")
    DeployStatus.objects.create(name="ERROR",
                                description="发布异常",
                                memo="发布异常")
    print('create all deploy status data')

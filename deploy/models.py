from django.db import models
from django.contrib.auth.models import User
from public.modules import CommonInfo
from appinput.models import App


IS_INC_TOT_CHOICES = (
    ('TOT', r'TOT'),
    ('INC', r'INC'),
)

DEPLOY_TYPE_CHOICES = (
    ('deployall', r'发布所有'),
    ('deploypkg', r'发布程序'),
    ('deploycfg', r'发布配置'),
    ('rollback', r'回滚'),
)


class DeployPool(CommonInfo):
    name = models.CharField(max_length=100,  blank=True, null=True, verbose_name="发布单编号")
    description = models.CharField(max_length=1024, blank=True, verbose_name="描述")
    app_name = models.ForeignKey(App, related_name='deploy_app', on_delete=models.CASCADE, verbose_name="APP应用")
    deploy_no = models.IntegerField(blank=True, null=True, default=0)
    branch_build = models.CharField(max_length=255, blank=True, null=True)
    jenkins_number = models.CharField(max_length=255, blank=True, null=True)
    code_number = models.CharField(max_length=255, blank=True, null=True)
    is_inc_tot = models.CharField(max_length=255, choices=IS_INC_TOT_CHOICES,
                                  blank=True, null=True,  verbose_name="全量或增量部署")
    deploy_type = models.CharField(max_length=255, choices=DEPLOY_TYPE_CHOICES,
                                   blank=True, null=True, verbose_name="发布程序或配置")
    salt_module_path = models.CharField(max_length=255, verbose_name="Salt APP路径")
    create_user = models.ForeignKey(User,  related_name='deploy_create_user', on_delete=models.CASCADE, verbose_name="创建用户")
    nginx_url = models.URLField(default=None, blank=True, null=True, verbose_name="Tengine URL")
    deploy_status = models.CharField(max_length=255, blank=True, null=True, verbose_name="发布单状态")
    deploy_progress = models.CharField(max_length=32, blank=True, null=True, verbose_name="发布单进度")



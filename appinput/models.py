from django.db import models
from django.contrib.auth.models import User
from public.modules import CommonInfo


class App(CommonInfo):
    """
    应用：
    """
    jenkins_job = models.CharField(max_length=255, verbose_name="JENKINS JOB名称")
    is_restart_status = models.BooleanField(default=True, verbose_name="是否重启")
    package_name = models.CharField(max_length=128, verbose_name="软件包名")
    op_log_no = models.IntegerField(blank=True, null=True, default=0)
    manage_user = models.ForeignKey(User, blank=True, null=True,
                                    related_name="manage_user", on_delete=models.CASCADE, verbose_name="APP管理员")
    script = models.CharField(max_length=65535, blank=True, null=True, verbose_name="APP服务脚本")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'App'
        ordering = ('-add_date',)

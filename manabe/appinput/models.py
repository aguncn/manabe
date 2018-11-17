from django.db import models
from django.contrib.auth.models import User
from public.models import CommonInfo
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class App(CommonInfo):
    """
    应用：
    """
    jenkins_job = models.CharField(max_length=255,
                                   verbose_name="JENKINS JOB名称")
    git_url = models.CharField(max_length=512,
                               verbose_name="Git地址")
    dir_build_file = models.CharField(max_length=512,
                                      verbose_name="编译目录")
    build_cmd = models.CharField(max_length=512,
                                 default="./",
                                 verbose_name="编译命令")
    is_restart_status = models.BooleanField(default=True,
                                            verbose_name="是否重启")
    package_name = models.CharField(max_length=128,
                                    blank=True,
                                    null=True,
                                    verbose_name="软件包名")
    zip_package_name = models.CharField(max_length=128,
                                        blank=True,
                                        null=True,
                                        verbose_name="压缩包名")
    op_log_no = models.IntegerField(blank=True,
                                    null=True,
                                    default=0)
    manage_user = models.ForeignKey(User,
                                    blank=True,
                                    null=True,
                                    related_name="manage_user",
                                    on_delete=models.CASCADE,
                                    verbose_name="APP管理员")
    script_url = models.CharField(max_length=128,
                                  blank=True,
                                  null=True,
                                  verbose_name="app脚本链接")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'App'
        ordering = ('-add_date',)

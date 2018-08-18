from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from appinput.models import App
from envx.models import Env
from public.modules import CommonInfo


class Server(CommonInfo):
    """
    服务器
    """
    ip_address = models.CharField(max_length=24, verbose_name="IP地址")
    salt_name = models.CharField(max_length=128, verbose_name="SaltStack minion")
    port = models.CharField(max_length=100, verbose_name="端口")
    app_name = models.ForeignKey(App,  related_name='app_name', on_delete=models.CASCADE, verbose_name="应用名")
    env_name = models.ForeignKey(Env, blank=True, null=True, related_name="server_env_name", on_delete=models.CASCADE, verbose_name="环境")
    app_user = models.CharField(max_length=24, blank=True, null=True, verbose_name="执行程序用户")
    op_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name="操作用户")
    app_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="程序包发送路径")
    salt_cmd = models.CharField(max_length=512, blank=True, null=True, verbose_name="执行脚本salt路径")
    history_deploy = models.CharField(max_length=512, blank=True, null=True, verbose_name="已部署版本")
    file_trans_status = models.BooleanField(default=False, verbose_name="传递发布文件是否成功")
    deploy_status = models.CharField(max_length=128, blank=True, null=True, verbose_name="发布状态(Err,Suc)")
    is_rollback = models.BooleanField(default=False)
    init_param = models.CharField(max_length=256, blank=True, null=True, verbose_name=u"构建参数")
    current_status = models.CharField(max_length=256, blank=True, null=True, default=u'正常', verbose_name=u"运行状态")

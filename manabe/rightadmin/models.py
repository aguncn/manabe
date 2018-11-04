from django.db import models
from public.models import CommonInfo
from django.contrib.auth.models import User
from envx.models import Env
from appinput.models import App
# Create your models here.


class Action(CommonInfo):
    aid = models.IntegerField(unique=True,
                              verbose_name="权限序号")


class Permission(CommonInfo):
    app_name = models.ForeignKey(App,
                                 related_name="pm_app_name",
                                 on_delete=models.CASCADE,
                                 verbose_name="APP应用")
    env_name = models.ForeignKey(Env,
                                 blank=True,
                                 null=True,
                                 related_name="pm_env_name",
                                 on_delete=models.CASCADE,
                                 verbose_name="环境")
    action_name = models.ForeignKey(Action,
                                    related_name="pm_action_name",
                                    on_delete=models.CASCADE,
                                    verbose_name="操作权限")
    main_user = models.ManyToManyField(User,
                                       blank=True,
                                       related_name="pm_user",
                                       verbose_name="操作用户")

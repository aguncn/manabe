from django.db import models
from public.modules import CommonInfo
# Create your models here.


class Env(CommonInfo):
    eid = models.IntegerField(unique=True, verbose_name="环境序号")
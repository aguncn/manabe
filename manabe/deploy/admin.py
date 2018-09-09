from django.contrib import admin

# Register your models here.

from . import models
admin.site.register(models.DeployPool)
admin.site.register(models.DeployStatus)
admin.site.register(models.History)
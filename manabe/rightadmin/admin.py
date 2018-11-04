from django.contrib import admin
# Register your models here.
from . import models

admin.site.register(models.Permission)
admin.site.register(models.Action)
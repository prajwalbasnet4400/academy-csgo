from django.contrib import admin
from . import models

admin.site.register(models.Server,admin.ModelAdmin)
admin.site.register(models.Vip,admin.ModelAdmin)
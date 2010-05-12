from django.db import models
from django.contrib import admin


class PrintMap(models.Model): 
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=200)
    _file = models.FileField(upload_to="media")


    def __unicode__(self):
        return u"%s" % self.title

class PrintMapAdmin(admin.ModelAdmin):
    pass

admin.site.register(PrintMap,PrintMapAdmin)

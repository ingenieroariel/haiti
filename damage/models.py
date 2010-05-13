from django.contrib.gis.db import models

# Create your models here.



class DamageMap(models.Model):
    title = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    guid = models.CharField(max_length=200)
    glide = models.CharField(max_length=200)
    pubdate = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    polygon = models.PointField()
    objects = models.GeoManager()

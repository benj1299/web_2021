from django.db import models
from django.contrib.gis.db import models

class Operators(models.Model):
    #id_zone     = models.IntegerField()
    adm_lb_nom	= models.CharField(max_length=20)
    generation	= models.CharField(max_length=20)
    statut	    = models.CharField(max_length=100)
    location = models.PointField("Location")
    sous_operator = models.CharField(max_length=100)
    image = models.CharField(max_length=250, blank=True)
    forfait = models.FloatField()
    link = models.CharField(max_length=250, blank=True)

class Meta:
    delimiter = ","
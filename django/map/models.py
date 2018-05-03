from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager

class Punkt(models.Model):
    nameOfProperty = models.CharField(max_length=100, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    point = models.PointField('longitude/latitude', geography=True, blank=True, null=True)
    
    def __str__(self):
        return self.nameOfProperty
    def __unicode__(self):
        return self.nameOfProperty

class Waypoint(models.Model):

    fastighetsbeteckning = models.CharField(max_length=32)
    area = models.IntegerField()
    
    geometry = models.PointField(srid=4326)

    def __unicode__(self):
        #return self.name
        return '%s %s %s' % (self.fastighetsbeteckning, self.geometry.x, self.geometry.y)

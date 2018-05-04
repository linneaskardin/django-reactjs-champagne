from django.db import models
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager

# THE MAP
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

# INFO FROM LANTMÄTERIET
class PropertyOwner(models.Model):
    reg_no = models.CharField('Organisationsnummer', null=True, max_length=13)
    coname = models.CharField('Firmanamn', max_length=300, default = None, null = True)
    jurform = models.CharField('Juridisk form', max_length=2, default = None, null = True)
    # Info regaring individuals. Might be omitted later /CE
    firstname = models.CharField('Förnamn', max_length=80, default = None, null = True)
    surname = models.CharField('Efternamn', max_length=100, default = None, null = True)
    class Meta:
        ordering = ('coname',) # Order by coname. Makes blank conames come first so it's not optimal /CE
    def __str__(self): # Good practise to use. Converts object to string /CE
        return (self.coname)

class Property(models.Model):
    coord_n = models.CharField('N-koordinat', max_length=30,default = None, null=True)
    coord_e= models.CharField('E-koordinat', max_length=30, default=None, null=True)
    owners = models.ManyToManyField(PropertyOwner)
    class Meta:
        ordering = ('coord_n',) # Order by northern coordinate /CE

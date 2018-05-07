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
    med_coord = models.PointField('Mediankoordinat',geography=True, srid=4326,blank=True, null=True)
    owners = models.ManyToManyField(PropertyOwner)

    def __unicode__(self):
        return '%s %s %s' % (self.med_coord.x, self.med_coord.y)
    
class PropertyBoarder(models.Model):
    internid = models.BigIntegerField()
    detaljtyp = models.CharField(max_length=10)
    gdat = models.CharField(max_length=16)
    adat = models.CharField(max_length=16)
    xyfel = models.BigIntegerField()
    metodplan = models.IntegerField()
    flyghojd = models.BigIntegerField()
    undskala = models.BigIntegerField()
    knid = models.IntegerField()
    geom = models.MultiLineStringField(srid=4326)
    
    def __unicode__(self):
        return self.internid

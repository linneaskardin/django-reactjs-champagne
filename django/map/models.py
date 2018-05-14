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
        ordering = ('coname', 'surname',) # Order by coname. Makes blank conames come first so it's not optimal /CE
    def __str__(self): # Good practise to use. Converts object to string /CE
        return (self.coname)

class LeaseHolder(models.Model): # Tomträttsinnehavare
    coname = models.CharField('Firmanamn', max_length=300, default = None, null = True)
    jurform = models.CharField('Juridisk form', max_length=2, default = None, null = True)
    # Info regaring individuals. Might be omitted later /CE
    firstname = models.CharField('Förnamn', max_length=80, default = None, null = True)
    surname = models.CharField('Efternamn', max_length=100, default = None, null = True)

class Property(models.Model):
    med_coord = models.PointField('Mediankoordinat',geography=True, srid=4326,blank=True, null=True)
    owners = models.ManyToManyField(PropertyOwner)
    leaseholders = models.ManyToManyField(LeaseHolder)
    area = models.DecimalField('Area',max_digits=24,decimal_places=12, default = 0, null=True)
    municipality = models.CharField('Kommun', max_length=16, default = '')
    district = models.CharField('Trakt', max_length=40, default = '')
    unity = models.CharField('Enhet', max_length=4, default = '')
    sign = models.CharField('Tecken', max_length=1, default = '', null = True)
    block = models.CharField('Block', max_length=4, default = '')
    price_fa = models.CharField('Köpeskilling fast egendom',max_length=36,default = '', null=True) # Comes as a string when missing
    currency_fa = models.CharField('Valuta fast egendom',max_length=5, default = '', null=True)
    price_lo = models.CharField('Köpeskilling lös egendom',max_length=36, default = '', null=True) # Comes as a string when missing
    currency_lo = models.CharField('Valuta lös egendom',max_length=5, default = '', null=True)
    price_date = models.CharField('Försäljningsdatum',max_length=8,null=True,default='')
    coord_e = models.DecimalField('Koord E', max_digits = 30, decimal_places=3, null = True, default = 0)
    coord_n = models.DecimalField('Koord N', max_digits = 30, decimal_places=3, null = True, default = 0)

    class Meta:
        ordering = ('coord_n', 'coord_e',) # Order by x Coord.
    def __unicode__(self):
        return '%s %s %s' % (self.med_coord.x, self.med_coord.y)

class PropertyBoarder(models.Model):
    internid = models.BigIntegerField()
    detaljtyp = models.CharField(max_length=11)
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

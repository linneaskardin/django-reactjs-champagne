# Create your views here.
from django.shortcuts import render #redirect
from django.views.generic import TemplateView

from django.template import loader
from django.http import HttpResponse
from .models import Property, PropertyBoarder, PropertyOwner, LeaseHolder
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.serializers import serialize
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry, Point

from pprint import pprint

def index(request):
    return render(request, 'map/index.html')

def property_datasets(request):
    print("i punkters view.")

    if (request.method == 'POST'):
        centerLat = float(request.POST.get('centerLat'))
        centerLng = float(request.POST.get('centerLng'))
        point = Point(centerLng, centerLat)
        pnt = GEOSGeometry(point, srid=4326)
        print(pnt)

        propertyGEOJson = serialize('geojson', Property.objects.filter(med_coord__distance_lte=(pnt, D(m=170)))) #the raidious given should be the same as in propertyOwner_datasets.
        return HttpResponse(propertyGEOJson, content_type='json')

def propertyOwner_datasets(request):
    print("i owners view")
   # if (request.method == 'POST'):
    centerLat = float(request.POST.get('centerLat'))
    centerLng = float(request.POST.get('centerLng'))
    point = Point(centerLng, centerLat)
    pnt = GEOSGeometry(point, srid=4326)
    print(pnt)

    thePropertiesInRange =Property.objects.filter(med_coord__distance_lte=(pnt, D(m=170))) #the raidious given should be the same as in property_datasets.
    ownersID = []
    for aProperty in thePropertiesInRange:
        theOwners = aProperty.owners.all()
        for owner in theOwners:
            ownersID.append(owner.pk)

    ownersGEOJson = serialize('geojson', PropertyOwner.objects.filter(pk__in=ownersID))
    return HttpResponse(ownersGEOJson, content_type='json')

def leaseHolder_datasets(request):

    centerLat = float(request.POST.get('centerLat'))
    centerLng = float(request.POST.get('centerLng'))
    point = Point(centerLng, centerLat)
    pnt = GEOSGeometry(point, srid=4326)
    print(pnt)

    thePropertiesInRange =Property.objects.filter(med_coord__distance_lte=(pnt, D(m=170))) #the raidious given should be the same as in property_datasets.
    leaseHoldersID = []

    for aProperty in thePropertiesInRange:

        theLeasers = aProperty.leaseholders.all()
        for leaser in theLeasers:
            leaseHoldersID.append(leaser.pk)

    leasersGEOJson = serialize('geojson', LeaseHolder.objects.filter(pk__in=leaseHoldersID))
    return HttpResponse(leasersGEOJson, content_type='json')

def propertyBoarder_datasets(request):

    centerLat = float(request.POST.get('centerLat'))
    centerLng = float(request.POST.get('centerLng'))
    point = Point(centerLng, centerLat)

    punkter = serialize('geojson', PropertyBoarder.objects.all())
    #punkter = serialize('geojson', PropertyBoarder.objects.filter(pk__gte=50000))
    return HttpResponse(punkter, content_type='json')




###########SPARAD KOD##########

#    punkter = serialize('geojson', PropertyOwner.objects.filter(pk__lte=100)) #gte = greater/equal than, lte = less/equal than
#    #punkter = serialize('geojson', Property.objects.all())
#    return HttpResponse(punkter, content_type='json')

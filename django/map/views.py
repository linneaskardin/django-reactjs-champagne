# Create your views here.
from django.shortcuts import render #redirect
from django.views.generic import TemplateView

from django.template import loader
from django.http import HttpResponse
from .models import Punkt, Waypoint, Property, PropertyBoarder, PropertyOwner, LeaseHolder
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.serializers import serialize
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry, Point

def index(request):
    return render(request, 'map/index.html')

def punkt_datasets(request):
    punkter = serialize('geojson', Punkt.objects.all())
    print (punkter)
    return HttpResponse(punkter, content_type='json')

def waypoint_datasets(request):
    waypoints = serialize('geojson', Waypoint.objects.all())
    return HttpResponse(waypoints, content_type='json')

def property_datasets(request):
    print("i punkters view.")

    if (request.method == 'POST'):
        centerLat = float(request.POST.get('centerLat'))
        centerLng = float(request.POST.get('centerLng'))
        
        point = Point(centerLng, centerLat)
        pnt = GEOSGeometry(point, srid=4326)
        print(pnt)
        
        print("jomjom")
        print(Property.objects.filter(med_coord__distance_lte=(pnt, D(m=200))))
        print("hejsvej")
        
        thePoints = serialize('geojson', Property.objects.filter(med_coord__distance_lte=(pnt, D(m=200)))) #the raidious given should be the same as in propertyOwner_datasets.
        return HttpResponse(thePoints, content_type='json')

def propertyOwner_datasets(request):
    print("i owners view")
   # if (request.method == 'POST'):
    centerLat = float(request.POST.get('centerLat'))
    centerLng = float(request.POST.get('centerLng'))
    
    point = Point(centerLng, centerLat)
    pnt = GEOSGeometry(point, srid=4326)
    print(pnt)

    thePropertiesInRange =Property.objects.filter(med_coord__distance_lte=(pnt, D(m=200))) #the raidious given should be the same as in property_datasets.
    propertiesID = []
    for aProperty in thePropertiesInRange:
        ownersPk=aProperty.pk
        propertiesID.append(ownersPk)
        #owners.append(PropertyOwner.objects.filter(pk__exact=ownersPk)) #16112 
    
    ownersGEOJson = serialize('geojson', PropertyOwner.objects.filter(pk__in=propertiesID)) 
    return HttpResponse(ownersGEOJson, content_type='json')

def leaseHolder_datasets(request):
    #punkter = serialize('geojson', Property.objects.all())
    punkter = serialize('geojson',  LeaseHolder.objects.filter(pk__lte=300)) #gte = greater/equal than, lte = less/equal than
    return HttpResponse(punkter, content_type='json')

def propertyBoarder_datasets(request):
    #punkter = serialize('geojson', PropertyBoarder.objects.all())
    punkter = serialize('geojson', PropertyBoarder.objects.filter(pk__gte=50000))
    return HttpResponse(punkter, content_type='json')


def makePointFromCoord():
    return null



###########SPARAD KOD##########


#    punkter = serialize('geojson', PropertyOwner.objects.filter(pk__lte=100)) #gte = greater/equal than, lte = less/equal than
#    #punkter = serialize('geojson', Property.objects.all())
#    return HttpResponse(punkter, content_type='json')

def googleKarta(request):
    print('views.py 1')
    return render(request, 'map/googleKartaData.html')
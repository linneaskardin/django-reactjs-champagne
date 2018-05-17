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
    #punkter = serialize('geojson', Property.objects.all())
    
    print("i punkters view.")

    
    if (request.method == 'POST'):
        print("i if")
        print("it is a POST-anrop i property-viewen")
        centerLat = float(request.POST.get('centerLat'))
        centerLng = float(request.POST.get('centerLng'))
        print(centerLat)
        print(centerLng)
        
        point = Point(centerLng, centerLat)
        pnt = GEOSGeometry(point, srid=4326)
        print(pnt)
        
        thePoints = serialize('geojson', Property.objects.filter(med_coord__distance_lte=(pnt, D(m=200))))
        return HttpResponse(thePoints, content_type='json')
    
#    else:
#        print("i else")
#        punkter = serialize('geojson', Property.objects.filter(pk__lte=30)) #gte = greater/equal than, lte = less/equal than
#        return HttpResponse(punkter, content_type='json')

def propertyOwner_datasets(request):
    #punkter = serialize('geojson', Property.objects.all())

    punkter = serialize('geojson', PropertyOwner.objects.filter(pk__lte=100)) #gte = greater/equal than, lte = less/equal than

    return HttpResponse(punkter, content_type='json')

def leaseHolder_datasets(request):
    #punkter = serialize('geojson', Property.objects.all())
    punkter = serialize('geojson',  LeaseHolder.objects.filter(pk__lte=300)) #gte = greater/equal than, lte = less/equal than
    return HttpResponse(punkter, content_type='json')

def propertyBoarder_datasets(request):
    #punkter = serialize('geojson', PropertyBoarder.objects.all())
    punkter = serialize('geojson', PropertyBoarder.objects.filter(pk__gte=50000))
    return HttpResponse(punkter, content_type='json')

def googleKarta(request):
    print('views.py 1')
    return render(request, 'map/googleKartaData.html')

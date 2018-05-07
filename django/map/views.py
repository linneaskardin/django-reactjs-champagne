# Create your views here.
from django.shortcuts import render #redirect
from django.views.generic import TemplateView

from django.template import loader
from django.http import HttpResponse
from .models import Punkt, Waypoint, PropertyBoarder, Property
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.serializers import serialize

def index(request):
    print('views.py 1')
    return render(request, 'map/index.html')

def punkt_datasets(request):
    print("views.py 1")
    punkter = serialize('geojson', Punkt.objects.all())
    print("views.py 2")
    print (punkter)
    return HttpResponse(punkter, content_type='json')

def waypoint_datasets(request):
    punkter = serialize('geojson', Waypoint.objects.all())
    return HttpResponse(punkter, content_type='json')

def property_datasets(request):
    punkter = serialize('geojson', Property.objects.filter(pk__gte=27000)) # gte = greater/equal to, lte = less/equal to
    return HttpResponse(punkter, content_type='json')

def propertyBoarder_datasets(request):
    punkter = serialize('geojson', PropertyBoarder.objects.all())
    return HttpResponse(punkter, content_type='json')

def googleKarta(request):
    print('views.py 1')
    return render(request, 'map/googleKartaData.html')

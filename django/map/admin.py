

# Register your models here.
from django.contrib import admin

from .models import Punkt, Waypoint

from django.contrib.gis.db import models
from django.contrib.gis import admin #från youtubevideo DjangoCon
from leaflet.admin import LeafletGeoAdmin

class PunktAdmin(LeafletGeoAdmin):
    list_display =('nameOfProperty', 'longitude', 'latitude', 'point') 
    
class WaypointAdmin(LeafletGeoAdmin):
    list_display =('fastighetsbeteckning', 'geometry') #Dessa är samma som de som finns i models.py Incidences. Skriver ut namnen istället för Incidences.object.123  


admin.site.register(Punkt, PunktAdmin)
admin.site.register(Waypoint, WaypointAdmin)

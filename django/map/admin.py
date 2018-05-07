

# Register your models here.
from django.contrib import admin

from .models import Punkt, Waypoint, PropertyOwner, Property, PropertyBoarder

from django.contrib.gis.db import models
from django.contrib.gis import admin #från youtubevideo DjangoCon
from leaflet.admin import LeafletGeoAdmin

# FOR THE MAP
class PunktAdmin(LeafletGeoAdmin):
    list_display =('nameOfProperty', 'longitude', 'latitude', 'point')

class WaypointAdmin(LeafletGeoAdmin):
    list_display =('fastighetsbeteckning', 'geometry') #Dessa är samma som de som finns i models.py Incidences. Skriver ut namnen istället för Incidences.object.123
# FOR THE DATA
class PropertyOwnerAdmin(admin.ModelAdmin): # Decides what is shown for PropertyOwner
    list_display=('coname', 'reg_no', 'firstname', 'surname')
    pass # Means that it shouldn't do anything with this class after 'pass'
class PropertyAdmin(admin.ModelAdmin):
  
    # Don't know how to display PointField
    pass

class PropertyBoarderAdmin(LeafletGeoAdmin):
    list_display =('adat', 'internid', 'detaljtyp', 'xyfel' )

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyOwner, PropertyOwnerAdmin)# Makes data appear on admin site
admin.site.register(Punkt, PunktAdmin)
admin.site.register(Waypoint, WaypointAdmin)
admin.site.register(PropertyBoarder, PropertyBoarderAdmin)

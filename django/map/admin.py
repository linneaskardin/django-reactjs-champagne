

# Register your models here.
from django.contrib import admin

from .models import PropertyOwner, Property, PropertyBoarder, LeaseHolder

from django.contrib.gis.db import models
from django.contrib.gis import admin #från youtubevideo DjangoCon
from leaflet.admin import LeafletGeoAdmin

class PropertyOwnerAdmin(admin.ModelAdmin): # Decides what is shown for PropertyOwner
    list_display=('coname', 'reg_no', 'firstname', 'surname')
    pass # Means that it shouldn't do anything with this class after 'pass'
class PropertyAdmin(admin.ModelAdmin):
    # Don't know how to display PointField
    pass
class LeaseHolderAdmin(admin.ModelAdmin):
    list_display=('coname', 'firstname', 'surname')
    pass

class PropertyBoarderAdmin(LeafletGeoAdmin):
    list_display =('adat', 'internid', 'detaljtyp', 'xyfel' )

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyOwner, PropertyOwnerAdmin)# Makes data appear on admin site
admin.site.register(LeaseHolder, LeaseHolderAdmin)
admin.site.register(PropertyBoarder, PropertyBoarderAdmin)

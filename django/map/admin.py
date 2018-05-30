

# Register your models here.
from django.contrib import admin

from .models import PropertyOwner, Property, PropertyBoarder, LeaseHolder

from django.contrib.gis.db import models
from django.contrib.gis import admin #learned from youtubevideo DjangoCon
from leaflet.admin import LeafletGeoAdmin

class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display=('coname', 'reg_no', 'firstname', 'surname')
    pass
class PropertyAdmin(admin.ModelAdmin):
    # Don't know how to display PointField
    pass
class LeaseHolderAdmin(admin.ModelAdmin):
    list_display=('coname', 'firstname', 'surname')
    pass

class PropertyBoarderAdmin(LeafletGeoAdmin):
    list_display =('adat', 'internid', 'detaljtyp', 'xyfel' )

admin.site.register(Property, PropertyAdmin) # Makes data appear on admin site
admin.site.register(PropertyOwner, PropertyOwnerAdmin)
admin.site.register(LeaseHolder, LeaseHolderAdmin)
admin.site.register(PropertyBoarder, PropertyBoarderAdmin)

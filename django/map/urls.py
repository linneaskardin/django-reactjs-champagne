from django.conf.urls import include, url
from django.urls import re_path, path
from djgeojson.views import GeoJSONLayerView
from map import views
from .views import punkt_datasets , waypoint_datasets


print("urls.py -map 1")

urlpatterns=[
    re_path('punkter_pa_karta', views.index, name='toolgate_maps'),
    re_path('punkters_data/', views.punkt_datasets, name='laddapunkter'),
    re_path('waypoints_data/', views.waypoint_datasets, name='laddawaypoints'), # properties=('fastighetsbeteckning', 'geometry'),

    re_path('propertyBorders_data/', views.propertyBoarder_datasets, name='laddaproperty'),
    re_path('properties_data/', views.property_datasets, name='laddapunkter'),
    
    re_path('punkter_pa_googlekarta', views.googleKarta),


print("urls.py -map 2")

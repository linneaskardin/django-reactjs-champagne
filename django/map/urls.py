from django.conf.urls import include, url
from django.urls import re_path
from djgeojson.views import GeoJSONLayerView
from map import views
from .views import punkt_datasets , waypoint_datasets


print("urls.py -map 1")

urlpatterns=[
    re_path('punkter_pa_karta', views.index, name='map-index'),
    re_path('punkters_data/', views.punkt_datasets, name='laddapunkter'),
    re_path('waypoints_data/', views.waypoint_datasets, name='laddawaypoints'), # properties=('fastighetsbeteckning', 'geometry'),    
]

print("urls.py -map 2")
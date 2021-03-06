from django.conf.urls import include, url
from django.urls import re_path, path
from djgeojson.views import GeoJSONLayerView
from map import views
from .views import propertyBoarder_datasets, leaseHolder_datasets


urlpatterns=[
    re_path('punkter_pa_karta', views.index, name='toolgate_maps'),
    re_path('properties_data/', views.property_datasets, name='laddaproperty'),
    re_path('propertyBorders_data/', views.propertyBoarder_datasets, name='laddapropertyboarders'),
    re_path('propertyOwners_data/', views.propertyOwner_datasets, name='laddapropertyowners'),
    re_path('leaseHolder_data/', views.leaseHolder_datasets, name='laddapropertyleaseholders'),
]

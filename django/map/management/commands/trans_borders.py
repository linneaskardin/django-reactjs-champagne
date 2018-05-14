# Script to translate property borders (shape-file) from SWEREF to WGS84
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Translates property borders (shape-file) from SWEREF to WGS84'
    def handle(self, *args, **options):
        import geopandas as gpd
        from django.contrib.gis.db import models
        import pyproj
        from map.models import PropertyBoarder
        import pandas as pd
        from shapely.geometry import multilinestring

        # Important that the shapefiles are copied into the project together as a zip-file
        fp = '/Users/claraengman/django-reactjs-champagne/django/data/al_get/al_get.shp' # Insert your own path
        borders_sweref = gpd.read_file(fp)
        borders_wgs84 = borders_sweref.to_crs({'init': 'epsg:4326'})
        df = pd.DataFrame(borders_wgs84)
        gdf = gpd.GeoDataFrame(df, geometry = df.geometry)
        # save the GeoDataFrame
        gdf.to_file("borders_wgs84.shp")
        self.stdout.write("Successfully translated shape-file and put it in the project with filenames borders_wgs84", ending='') # This is the way to print in the console //CE

import os
from django.contrib.gis.utils import LayerMapping
#import mpl_toolkits.basemap.pyproj as pyproj #så har Clara skrivit den
from django.contrib.gis.db import models
import pyproj
from .models import PropertyBoarder

propertyBoarder_mapping = {
    'internid': 'INTERNID',
    'detaljtyp': 'DETALJTYP',
    'gdat': 'GDAT',
    'adat': 'ADAT',
    'xyfel': 'XYFEL',
    'metodplan': 'METODPLAN',
    'flyghojd': 'FLYGHOJD',
    'undskala': 'UNDSKALA',
    'knid': 'KNID',
    'geom': 'MULTILINESTRING',
}

propertyBoarder_shp = os.path .abspath(os.path.join(os.path.dirname(__file__),'data/borders_wgs84.shp'))

def run(verbose=True):
    lm = LayerMapping(PropertyBoarder, propertyBoarder_shp, propertyBoarder_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)
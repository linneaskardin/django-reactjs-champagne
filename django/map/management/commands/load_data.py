# Run by typing python manage.py load_data
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    help = 'Populates models'

    def handle(self, *args, **options):
        # Put everything that was originally in the python script. Can't include functions.
        # Everything needs to be indented //CE
        import pyproj
        from map.models import Property, PropertyOwner
        from django.contrib.gis.geos import Point
        import csv
        # Import data for coordinates
        csvkoord= open('data/MEDIAN_09M.txt', 'r', encoding='mac_roman', newline='') # Need encoding mac_roman and newline=''. Don't know why //CE
        readerkoord = csv.reader(csvkoord, delimiter=';')
        d={} # create dictionary to connect data
        wgs84=pyproj.Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
        SWEREF99=pyproj.Proj("+init=EPSG:3006") # SWEREF 99 TM system
        for row in readerkoord:
            # Define projections using EPSG codes
            wgs_e, wgs_n = pyproj.transform(SWEREF99,wgs84, row[6], row[5])
            # Create Point
            pnt = Point(wgs_e, wgs_n)
            d[row[3]] = {'med_coord':pnt, 'coord_e':row[6], 'coord_n':row[5]} # Populate dictionary
        csvkoord.close() # VERY important to close!
        # Import data for Property Owners
        csvlag = open('data/LAGFP_35S.txt','r', encoding='mac_roman',newline='')
        readerl = csv.reader(csvlag, delimiter=';')
        e={} # create dictionary to connect data
        for row in readerl:
            e[row[20]] = {'org_nr':row[21],
            'fornamn':row[23], 'efternamn':row[25],'irfast':row[17],
            'jurform':row[26], 'firmanamn':row[27]}
        csvlag.close()
        z = {}
        for key,value in e.items():# iterator over e
            if key in d: # some PropertyOwners don't have coordinates
                value = {**d[key], **e[key]} # pull values and merge them
                z[key] = value # add the new values to z
        csvar = open('data/AREAL_08A.txt','r', encoding='mac_roman',newline='')
        readera = csv.reader(csvar, delimiter=';')
        f={} # create dictionary to connect data
        for row in readerl:
            e[row[20]] = {'org_nr':row[21],
            'fornamn':row[23], 'efternamn':row[25],'irfast':row[17],
            'jurform':row[26], 'firmanamn':row[27]}
        csvar.close()
        # populate database tables
        for key,value in z.items():
            q = PropertyOwner(reg_no=z.get(key,{'org_nr':'NA'})['org_nr'],
            firstname=z.get(key,{'fornamn':'NA'})['fornamn'],surname=z.get(key,{'efternamn':'NA'})['efternamn'],
            coname=z.get(key,{'firmanamn':'NA'})['firmanamn'],jurform=z.get(key,{'jurform':'NA'})['jurform'])
            q.save()
            y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
            coord_n=z.get(key,{'coord_n':'NA'})['coord_n'])
            y.save()
            y.owners.add(q)
        self.stdout.write("Successfully populated models", ending='') # This is the way to print in the console //CE

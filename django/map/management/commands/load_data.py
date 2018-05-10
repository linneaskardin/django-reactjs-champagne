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
        dictCoord={} # create dictionary to connect data
        wgs84=pyproj.Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
        SWEREF99=pyproj.Proj("+init=EPSG:3006") # SWEREF 99 TM system
        for row in readerkoord:
            # Define projections using EPSG codes
            wgs_e, wgs_n = pyproj.transform(SWEREF99,wgs84, row[6], row[5])
            # Create Point
            pnt = Point(wgs_e, wgs_n)
            dictCoord[row[3]] = {'med_coord':pnt, 'coord_e':row[6], 'coord_n':row[5]} # Populate dictionary
        csvkoord.close() # VERY important to close!
        # Import data for Property Owners
        csvlag = open('data/LAGFP_35S.txt','r', encoding='mac_roman',newline='')
        readerl = csv.reader(csvlag, delimiter=';')
        dictOwner={} # create dictionary to connect data
        for row in readerl:
            dictOwner[row[20]] = {'reg_nr':row[21],
            'firstname':row[23], 'surname':row[25],'irfast':row[17],
            'jurform':row[26], 'coname':row[27]}
        csvlag.close()
        csvar = open('data/AREAL_08A.txt','r', encoding='mac_roman',newline='')
        readera = csv.reader(csvar, delimiter=';')
        dictArea={}
        for row in readera:
            dictArea[row[3]] = {'area':row[7]}
        csvar.close()
        csvreg = open('data/REGENH_01A.txt','r', encoding='mac_roman',newline='')
        readerr = csv.reader(csvreg, delimiter=';')
        dictPropNo={}
        for row in readerr:
            dictPropNo[row[3]] = {'municipality':row[6],'district':row[7],'block':row[8],'sign':row[9],'unity':row[10]}
        csvreg.close()
        z = {}
        for key,value in dictOwner.items():# iterator over e
            if key in dictCoord: # some PropertyOwners don't have coordinates
                if key in dictArea:
                    value = {**dictCoord[key], **dictOwner[key], **dictPropNo, **dictArea} # pull values and merge them
#                if key in dictArea and key in dictPropNo:
#                    value = {**dictCoord[key],**dictOwner[key],**dictArea[key],**dictPropNo[key]}
#                elif key in dictArea and key not in dictPropNo:
#                    value = {**dictCoord[key],**dictOwner[key],**dictArea[key]}
#                elif key not in dictArea and key in dictPropNo:
#                    value = {**dictCoord[key],**dictOwner[key],**dictPropNo[key]}
                else:
                    value = {**dictCoord[key], **dictOwner[key], **dictPropNo} # pull values and merge them
                z[key] = value # add the new values to z
        # populate database tables
        for key,value in z.items():
            q = PropertyOwner(reg_no=z.get(key,{'reg_nr':'NA'})['reg_nr'],
            firstname=z.get(key,{'firstname':'NA'})['firstname'],surname=z.get(key,{'surname':'NA'})['surname'],
            coname=z.get(key,{'coname':'NA'})['coname'],jurform=z.get(key,{'jurform':'NA'})['jurform'])
            q.save()
            if key in dictArea:
                y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], area=z.get(key,{'area':'NA'})['area'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                unity=z.get(key,{'unity':'NA'})['unity'])
#            elif key in dictArea and key not in dictPropNo:
#                y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
#                coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], area=z.get(key,{'area':'NA'})['area'])
            else:
                y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                coord_n=z.get(key,{'coord_n':'NA'})['coord_n'],area=0,municipality=z.get(key,{'municipality':'NA'})['municipality'],
                district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                unity=z.get(key,{'unity':'NA'})['unity']) # Area becomes 0 when info of the area doesn't exist
            y.save()
            y.owners.add(q)
        self.stdout.write("Successfully populated models", ending='') # This is the way to print in the console //CE

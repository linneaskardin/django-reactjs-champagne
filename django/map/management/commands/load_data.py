# Run by typing python manage.py load_data
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    help = 'Populates model fields'

    def handle(self, *args, **options):
        import pyproj
        from map.models import Property, PropertyOwner, LeaseHolder
        from django.contrib.gis.geos import Point
        import csv
        # Import data for coordinates
        with open('data/MEDIAN_09M.txt', 'r', encoding='iso-8859-1', newline='') as csvmed: # Need encoding mac_roman and newline=''. Don't know why //CE
            readerkoord = csv.reader(csvmed, delimiter=';')
            dictCoord={} # create dictionary to connect data
            wgs84=pyproj.Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
            SWEREF99=pyproj.Proj("+init=EPSG:3006") # SWEREF 99 TM system
            for row in readerkoord:
            # Define projections using EPSG codes
                wgs_e, wgs_n = pyproj.transform(SWEREF99,wgs84, row[6], row[5])
            # Create Point
                pnt = Point(wgs_e, wgs_n)
                dictCoord[row[3]] = {'med_coord':pnt, 'coord_e':row[6], 'coord_n':row[5]} # Populate dictionary
        # Import data for Property Owners and place in dictionary
        with open('data/LAGFP_35S.txt','r', encoding='iso-8859-1',newline='') as csvlag:
            readerl = csv.reader(csvlag, delimiter=';')
            dictOwner={} # create dictionary to connect data
            for row in readerl:
                dictOwner[row[20]] = {'reg_nr':row[21],'firstname':row[23], 'surname':row[25],'jurform':row[26], 'coname':row[27]}
        # Import data for Area and place in dictionary
        with open('data/AREAL_08A.txt','r', encoding='iso-8859-1',newline='') as csvar:
            readera = csv.reader(csvar, delimiter=';')
            dictArea={}
            for row in readera:
                dictArea[row[3]] = {'area':row[7]}
        # Import data for Property Number and place in dictionary
        with open('data/REGENH_01A.txt','r', encoding='iso-8859-1',newline='') as csvreg:
            readerr = csv.reader(csvreg, delimiter=';')
            dictPropNo={}
            for row in readerr:
                dictPropNo[row[3]] = {'municipality':row[6],'district':row[7],'block':row[8],'sign':row[9],'unity':row[10]}
        # Import data for Property Leaseholders and place in dictionary
        with open('data/TOMTRP_35T.txt','r', encoding='iso-8859-1',newline='') as csvtom:
            readert = csv.reader(csvtom, delimiter=';')
            dictLease={}
            for row in readert:
                if row[20] is not None: # It might be None
                    dictLease[row[20]] = {'firstname_l':row[23], 'surname_l':row[25], 'coname_l':row[27],'irfast_uuid':row[17]}
        # Import data for Taxation value and place in dictionary
        with open('data/TAXENH_40A.txt','r', encoding='iso-8859-1',newline='') as csvar:
            readerta = csv.reader(csvar, delimiter=';')
            dictTax={}
            for row in readerta:
                dictTax[row[3]] = {'taxation_year':row[15],'taxation_land':row[11],'taxation_build':row[12]}
        # Import data for Price and place in dictionary
        # Connection table between KOPESK and Property
        with open('data/FASTAGF_35O.txt','r', encoding='iso-8859-1',newline='') as csvfas:
            readerf = csv.reader(csvfas, delimiter=';')
            dictFas={}
            for row in readerf:
                if row[5] is not None: # It might be None
                    dictFas[row[5]] = {'fnr':row[7],'irfast_uuid':row[6],'kopesk_uuid':row[5]}
        with open('data/KOPESK_35P.txt','r', encoding='iso-8859-1',newline='') as csvkop:
            readerk = csv.reader(csvkop, delimiter=';')
            dictKopProp={}
            dictKopLease={}
            for row in readerk:
                if row[3] in dictFas:
                    u = dictFas.get(row[3],{'irfast_uuid':'NA'})['irfast_uuid']
                    for key,value in dictLease.items():
                        v = dictLease.get(key,{'irfast_uuid':'NA'})['irfast_uuid']
                        if u == v:
                            dictKopLease[row[3]] = {'currency_fa':row[9],'price_fa':row[10],'currency_lo':row[15],'price_lo':row[16],'price_date':row[1][:8]} # Don't include serial number
                        elif u is 'NA':
                            pass
                        elif v is 'NA':
                            pass
                        else:
                            dictKopProp[row[3]] = {'currency_fa':row[9],'price_fa':row[10],'currency_lo':row[15],'price_lo':row[16],'price_date':row[1][:8]}
        # Merge dictKopProp and dictFas
        d = {}
        for key,value in dictKopProp.items():
            if key in dictFas:
                value = {**dictKopProp[key], **dictFas[key]}
                d[key] = value
        # Merge dictKopProp and dictFas
        e = {}
        for key,value in dictKopLease.items():
            if key in dictFas:
                value = {**dictKopProp[key], **dictFas[key]}
                e[key] = value
        # Create dictPrice and dictPriceLease with fnr as a key
        dictPrice = {}
        dictPriceLease = {}

        for key,value in d.items():
            dictPrice[d.get(key,{'fnr':'NA'})['fnr']] = {'currency_fa':d.get(key,{'currency_fa':'NA'})['currency_fa'],
            'price_fa':d.get(key,{'price_fa':'NA'})['price_fa'],'currency_lo':d.get(key,{'currency_lo':'NA'})['currency_lo'],
            'price_lo':d.get(key,{'price_lo':'NA'})['price_lo'],'price_date':d.get(key,{'price_date':'NA'})['price_date']}

            dictPriceLease[e.get(key,{'fnr':'NA'})['fnr']] = {'currency_fa':e.get(key,{'currency_fa':'NA'})['currency_fa'],
            'price_fa':e.get(key,{'price_fa':'NA'})['price_fa'],'currency_lo':e.get(key,{'currency_lo':'NA'})['currency_lo'],
            'price_lo':e.get(key,{'price_lo':'NA'})['price_lo'],'price_date':e.get(key,{'price_date':'NA'})['price_date']}

        # Merge all dictionaries according to what fields exists for the specific fnr
        z = {}
        for key,value in dictOwner.items():# iterator over e
            if key in dictCoord: # some PropertyOwners don't have coordinates
                if key in dictArea and key in dictPrice:
                    if key in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key], **dictLease[key],**dictPriceLease[key],**dictTax[key]} # pull values and merge them
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key], **dictLease[key],**dictPriceLease[key]}
                    elif key in dictLease and key not in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key], **dictLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key], **dictLease[key]}
                    elif key not in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key], **dictPriceLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key], **dictPriceLease[key]}
                    else:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPrice[key]}

                elif key in dictArea and key not in dictPrice:
                    if key in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictLease[key],**dictPriceLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictLease[key],**dictPriceLease[key]}
                    elif key in dictLease and key not in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictLease[key]}
                    elif key not in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPriceLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key], **dictPriceLease[key]}
                    else:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictArea[key]}

                elif key not in dictArea and key in dictPrice:
                    if key in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key], **dictLease[key],**dictPriceLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key], **dictLease[key],**dictPriceLease[key]}
                    elif key in dictLease and key not in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key], **dictLease[key], **dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key], **dictLease[key]}
                    elif key not in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key], **dictPriceLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key], **dictPriceLease[key]}
                    else:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPrice[key]}

                else:
                    if key in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictLease[key],**dictPriceLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictLease[key],**dictPriceLease[key]}
                    elif key in dictLease and key not in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictLease[key]}
                    elif key not in dictLease and key in dictPriceLease:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPriceLease[key],**dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictPriceLease[key]}
                    else:
                        if key in dictTax:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key], **dictTax[key]}
                        else:
                            value = {**dictCoord[key], **dictOwner[key], **dictPropNo[key]}
                z[key] = value # add the new values to z
        # Populate model fields
        for key,value in z.items():
            q = PropertyOwner(reg_no=z.get(key,{'reg_nr':'NA'})['reg_nr'],
            firstname=z.get(key,{'firstname':'NA'})['firstname'],surname=z.get(key,{'surname':'NA'})['surname'],
            coname=z.get(key,{'coname':'NA'})['coname'])
            q.save()
            if key in dictArea and key in dictPrice:
                if key in dictTax:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], area=z.get(key,{'area':'NA'})['area'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'],price_fa=z.get(key,{'price_fa':'NA'})['price_fa'],currency_fa=z.get(key,{'currency_fa':'NA'})['currency_fa'],
                    price_lo=z.get(key,{'price_lo':'NA'})['price_lo'],currency_lo=z.get(key,{'currency_lo':'NA'})['currency_lo'],price_date=z.get(key,{'price_date':'NA'})['price_date'],
                    taxation_land=z.get(key,{'taxation_land':'NA'})['taxation_land'],taxation_build=z.get(key,{'taxation_build':'NA'})['taxation_build'],taxation_year=z.get(key,{'taxation_year':'NA'})['taxation_year'])
                else:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], area=z.get(key,{'area':'NA'})['area'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'],price_fa=z.get(key,{'price_fa':'NA'})['price_fa'],currency_fa=z.get(key,{'currency_fa':'NA'})['currency_fa'],
                    price_lo=z.get(key,{'price_lo':'NA'})['price_lo'],currency_lo=z.get(key,{'currency_lo':'NA'})['currency_lo'],price_date=z.get(key,{'price_date':'NA'})['price_date'])
            # Fields that don't exist become None
            elif key in dictArea and key not in dictPrice:
                if key in dictTax:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], area=z.get(key,{'area':'NA'})['area'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'],taxation_land=z.get(key,{'taxation_land':'NA'})['taxation_land'],
                    taxation_build=z.get(key,{'taxation_build':'NA'})['taxation_build'],taxation_year=z.get(key,{'taxation_year':'NA'})['taxation_year'])
                else:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], area=z.get(key,{'area':'NA'})['area'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'])
            elif key not in dictArea and key in dictPrice:
                if key in dictTax:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'],price_fa=z.get(key,{'price_fa':'NA'})['price_fa'],currency_fa=z.get(key,{'currency_fa':'NA'})['currency_fa'],
                    price_lo=z.get(key,{'price_lo':'NA'})['price_lo'],currency_lo=z.get(key,{'currency_lo':'NA'})['currency_lo'],price_date=z.get(key,{'price_date':'NA'})['price_date'],
                    taxation_land=z.get(key,{'taxation_land':'NA'})['taxation_land'],taxation_build=z.get(key,{'taxation_build':'NA'})['taxation_build'],
                    taxation_year=z.get(key,{'taxation_year':'NA'})['taxation_year'])
                else:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'],price_fa=z.get(key,{'price_fa':'NA'})['price_fa'],currency_fa=z.get(key,{'currency_fa':'NA'})['currency_fa'],
                    price_lo=z.get(key,{'price_lo':'NA'})['price_lo'],currency_lo=z.get(key,{'currency_lo':'NA'})['currency_lo'],price_date=z.get(key,{'price_date':'NA'})['price_date'])
            else:
                if key in dictTax:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'],taxation_land=z.get(key,{'taxation_land':'NA'})['taxation_land'],taxation_build=z.get(key,{'taxation_build':'NA'})['taxation_build'],
                    taxation_year=z.get(key,{'taxation_year':'NA'})['taxation_year'])
                else:
                    y = Property(med_coord=z.get(key,{'med_coord':'NA'})['med_coord'], coord_e=z.get(key,{'coord_e':'NA'})['coord_e'],
                    coord_n=z.get(key,{'coord_n':'NA'})['coord_n'], municipality=z.get(key,{'municipality':'NA'})['municipality'],
                    district=z.get(key,{'district':'NA'})['district'],block=z.get(key,{'block':'NA'})['block'],sign=z.get(key,{'sign':'NA'})['sign'],
                    unity=z.get(key,{'unity':'NA'})['unity'])
            y.save()
            y.owners.add(q)
            if key in dictLease:
                if key in dictPriceLease:
                    l = LeaseHolder(firstname=z.get(key,{'firstname_l':'NA'})['firstname_l'],surname=z.get(key,{'surname_l':'NA'})['surname_l'],
                    coname=z.get(key,{'coname_l':'NA'})['coname_l'],price_fa=z.get(key,{'price_fa':'NA'})['price_fa'],
                    currency_fa=z.get(key,{'currency_fa':'NA'})['currency_fa'],price_lo=z.get(key,{'price_lo':'NA'})['price_lo'],
                    currency_lo=z.get(key,{'currency_lo':'NA'})['currency_lo'],price_date=z.get(key,{'price_date':'NA'})['price_date'])
                else:
                    l = LeaseHolder(firstname=z.get(key,{'firstname_l':'NA'})['firstname_l'],surname=z.get(key,{'surname_l':'NA'})['surname_l'],
                    coname=z.get(key,{'coname_l':'NA'})['coname_l'])
                l.save()
                y.leaseholders.add(l)

        self.stdout.write("Successfully populated models", ending='') # This is the way to print in the console //CE

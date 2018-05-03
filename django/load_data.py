# Script for populating database. If you cannot run the script from the terminal by placing the script in the project
# and writing load_data.py, you have to exectute the colorful lines one by one in python manage.py shell.
#If that's the case, the for-loops must be executed by themselves.
# It's important to have the .txt-files inside the project //CE

# Function for translating coordinates from SWEREF99 TM to wgs84 /CE
def transCoords(x,y):
    from mpl_toolkits.basemap import pyproj as pyproj # If you don't have basemap you could do as Ingrid does instead /CE
    # Define projections using EPSG codes
    wgs84=pyproj.Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
    SWEREF99=pyproj.Proj("+init=EPSG:3006") # SWEREF 99 TM system
    #UTM33N=pyproj.Proj("+init=EPSG:32633") # UTM coords, zone 33N Corresponds to Sweden
    e, n = pyproj.transform(SWEREF99,wgs84, x, y)
    return (e,n)

from map.models import Property, PropertyOwner
import csv
# Import data for coordinates
csvkoord= open('MEDIAN_09M.txt', 'r', encoding='mac_roman', newline='') # Need encoding mac_roman and newline=''. Don't know why //CE
readerkoord = csv.reader(csvkoord, delimiter=';')
d={} # create dictionary to connect data
for row in readerkoord:
    wgsCoords = transCoords(row[6],row[5]) # Translate from SWEREF99 to wgs84
    d[row[3]] = {'coorde':wgsCoords[0], 'coordn':wgsCoords[1]} # Populate dictionary
csvkoord.close() # VERY important to close!
# Import data for Property Owners
csvlag = open('LAGFP_35S.txt','r', encoding='mac_roman',newline='')
readerl = csv.reader(csvlag, delimiter=';')
e={} # create dictionary to connect data
for row in readerl:
    e[row[20]] = {'org_nr':row[21],
    'fornamn':row[23], 'efternamn':row[25],'irfast':row[17],
    'jurform':row[26], 'firmanamn':row[27]}
csvlag.close()
#csvtomt = open('TOMTRP_35T.txt','r', encoding='mac_roman',newline='')
#readert = csv.reader(csvtomt, delimiter=';')
#f = {}
#for row in readert:
#    f[row[20]] = {'fornamn':row[23], 'efternamn':row[25],
#    'jurform':row[26], 'firmanamn':row[27]}
#csvtomt.close()

# Merge data into 1 dictionary
z = {}
for key,value in e.items():# iterator over e
    if key in d: # some PropertyOwners don't have coordinates
        value = {**d[key], **e[key]} # pull values and merge them
        z[key] = value # add the new values to z
# populate database tables
for key,value in z.items():
    q = PropertyOwner(reg_no=z.get(key,{'org_nr':'NA'})['org_nr'],
    firstname=z.get(key,{'fornamn':'NA'})['fornamn'],surname=z.get(key,{'efternamn':'NA'})['efternamn'],
    coname=z.get(key,{'firmanamn':'NA'})['firmanamn'],jurform=z.get(key,{'jurform':'NA'})['jurform'])
    q.save()
    y = Property(coord_n=z.get(key,{'coordn':'NA'})['coordn'],coord_e=z.get(key,{'coorde':'NA'})['coorde'])
    y.save()
    y.owners.add(q)

#w = {} # empty dictonary for the leasehold rights //CE
#for key,value in f.items():
#    if key in z:
#        value = {**z[key], **e[key]}
#        w[key] = value

# Don't know how to connect Properties with Leaseholders
#for key,value in w.items():
#    a = Leaseholder(firstname=z.get(key,{'fornamn':'NA'})['fornamn'],surname=z.get(key,{'efternamn':'NA'})['efternamn'],
#    coname=z.get(key,{'firmanamn':'NA'})['firmanamn'],jurform=z.get(key,{'jurform':'NA'})['jurform'])
#    a.save()
#    y = Property.get(id=)
#    y.leaseholders.add(a)

# Connect the many-to-many relationship
#for i in Fastighetsagare.objects.all():
#    u = Fastighet.objects.get(fnr=i.fnr)
#    i.fastigheter.add(u)

# Test med enklare databas
#a1 = Fastighet(koord_n = '3555', koord_e = '2345')
#a1.save()
#a2 = Fastighetsagare(org_nr='1323444', fornamn='Fi', efternamn = 'Ding', firmanamn = 'Japp', fastighet=a1)
#a2.save()
#r = a2.fastighet
#new_a = r.fastighet_set.create(org_nr = '23455', fornamn='Kalle', efternamn = 'Vissna', firmanamn = 'Johi')
#new_a2 = Fastighetsagare.objects.create(org_nr = '2344', fornamn='Dan', efternamn = 'Fing', firmanamn = 'Akta', fastighet=a1)
#r.fastighet_set.add(new_a2)
#a3 = Fastighetsagare(org_nr='234535', fornamn='Slim', efternamn = 'Film', firmanamn = 'Sjö', fastighet=a1)
#a3.save()
#a4 = Fastighet(koord_n = '13445', koord_e = '134489')
#a4.save()

# Delete all data
#    Fastighetsagare.objects.all().delete()

#q = Fastighet.objects.all()
#y = Fastighetsagare.objects.all()
#for i in len(q):

# ---- SPARA TILL SENARE ----
#csvregen= open('REGENH_01A.txt', 'r', encoding='mac_roman', newline='') # Need encoding mac_roman and newline=''. Don't know why //CE
#readerr = csv.reader(csvregen, delimiter=';')
#d={}
#for row in readerr:
#    d[row[39]] = {'block':row[8],'trakt':row[7],'tkn':row[9], 'enhet':row[10]}
#csvregen.close()
#csvir=open('IRFAST_31A.txt', 'r', encoding='mac_roman', newline='')
#readeri = csv.reader(csvir, delimiter=';')
#e={}
#for row in readeri:
#    e[row[5]] = {'uuid':row[3]}
#csvir.close()
#z = {} # empty dict
#for key, value in e.items():  # iterator over e
#    value = { **d[key], **e[key] }  # pull values and and merge them
#    z[key] = value
#csvlag.close()
##for key,dict in f.items():
##    q = Fastighetsagare(org_nr=row[21],fornamn=row[23],efternamn=row[25], firmanamn=row[27]) # Kolumnnumret blir en mindre eftersom det börjar på 0
##    q.save()

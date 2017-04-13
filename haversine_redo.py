import json
import numpy as np
import pandas as pd
import os
import csv

def haversine_np(x):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1 = x[0][0]
    print lon1
    print type(lon1)
    lat1 = x[0][1]
    lon2 = x[1][0]
    lat2 = x[1][1]
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km
    

path = "H:/CLASS/GTECH734/TestFolder"
dirs = os.listdir( path )
for file in dirs:
    filename = file
filecsv = "H:/CLASS/GTECH734/TestFolder/"+str(filename)  
results ={"type":"FeatureCollection","features":[]}
x={}
featurelist = []
lonlatlist = []
latlonlist = [] 
with open(filecsv) as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        print type(row[1])
        print type(row[2])
        lonlatlist.append([(row[1],row[2]),row[25]])
    lonlatlist =sorted(lonlatlist, key=lambda x: x[1])
    for listlon in lonlatlist:
        latlon=(listlon[0])
        latlonlist.append(latlon)


lonLatLength = len(latlonlist)
for i in range(1,lonLatLength-1):
    valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":""} }
    a = i
    b = i + 1
    x=latlonlist[a],latlonlist[b]
    print x
    print type (x[0][0])
    print x[0][0]
    distance = haversine_np(x)
    valuedict["geometry"]["coordinates"] =x
    valuedict["properties"]["distance"] = distance
    featurelist.append(valuedict)
results["features"] = featurelist
geojson = json.dumps(results)
print geojson
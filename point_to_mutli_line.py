import psycopg2
import json
import numpy as np
import pandas as pd


def gpsroute():
    pgcnxn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    cursor = pgcnxn.cursor()
    query="SELECT longitude, latitude FROM oct18_K082 ORDER BY odometer asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    results ={"type":"FeatureCollection","features":[]}
    x={}
    featurelist = []
    lonlatlist = []

    for row in rows:
        lonlatlist.append([float(row[0]),float(row[1])])
    print lonlatlist
    
    lonLatLength = len(lonlatlist)
    for i in range(1,lonLatLength-1):
        valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":""} }
        a = i
        b = i + 1
        x=lonlatlist[a],lonlatlist[b]
        distance = haversine_np(x)
        valuedict["geometry"]["coordinates"] =x
        valuedict["properties"]["distance"] = distance
        featurelist.append(valuedict)
    results["features"] = featurelist
    with open("apriltest.geojson", 'w') as outfile:
        json.dump(results, outfile)
    outfile.close()

def haversine_np(x):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1 = x[0][0]
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


gpsroute()
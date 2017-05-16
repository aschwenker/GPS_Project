import json
import numpy as np
from datetime import datetime
import csv
import os

def isTimeFormat(input):
    """allows us to determine the date format for further processes"""
    try:
        datetime.strptime(input, '%m/%d/%Y %H:%M:%S')
        return True
    except ValueError:
        return False


def haversine_np(x):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """

    lon1 = float(x[0][0])
    lat1 = float(x[0][1])
    lon2 = float(x[1][0])
    lat2 = float(x[1][1])
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km
    
    
def gpsroute(csvdestination,jsondestination):
    """Takes in the gps data as a list, reads it and enriches it.
    then returns a geojson feature collection of line segments between each lat,lon given"""

    results ={"type":"FeatureCollection","features":[]}
    x={}
    featurelist = []
    lonlatlist = []
    latlonlist = []
    timeheader = ''
    with open(csvdestination,'r') as csvfile:
        headerreader = csv.reader(csvfile)
        headers = headerreader.next()
    csvfile.close()
    for header in headers:
        if 'time' in header.lower():
            timeheader = header
        if 'lat' in header.lower():
            latheader = header
        if 'lon' in header.lower():
            lonheader = header
    with open(csvdestination,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            timeraw=row[timeheader]
            if isTimeFormat(timeraw):       
                time = datetime.strptime(timeraw,"%m/%d/%Y %H:%M:%S")
                lonlatlist.append([[row[lonheader],row[latheader]],time])
            else:
                time = datetime.strptime(timeraw,"%m/%d/%Y %H:%M")
                lonlatlist.append([[row[lonheader],row[latheader]],time])
            #appends to a list to the list: [[lat, lon ],time]
            #necessary becuase couldnt perform following sort if it were a tuple
    lonlatlist =sorted(lonlatlist, key=lambda x: x[1])
    #sorts on time
    for listlon in lonlatlist:
        latlon=((float(listlon[0][0]),float(listlon[0][1])))
        #tuple
        time = listlon[1]
        appenditem=([latlon,time])
        #restructuring format
        latlonlist.append(appenditem)
        #list of ((lat,lon),time)
    
    for i in range(0,len(latlonlist)-1):
        #must be range(len-1) to accomodate line segment lat/lon pairs
        valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":"","speed":"","duration":""} }
        #creates dictionary that will populate feature list of dict created above
        x=latlonlist[i][0],latlonlist[i+1][0]
        #((lon,lat),(lon,lat)) (tuple,tuple) represents start & end of line seg
        distance = round(haversine_np(x),2)
        time = latlonlist[i+1][1]-latlonlist[i][1]
        #start and end time for seg
        print (float(time.seconds))
        duration = ((float(time.seconds))/3600)
        #converts to hours
        print duration
        if float(duration) > 0:
            print float(distance),"/",float(duration)
            speed = round((float(distance)/float(duration)),2)
        else:
            speed = 0
        x=latlonlist[i][0],latlonlist[i+1][0]
        valuedict["geometry"]["coordinates"] =x
        valuedict["properties"]["distance"] = distance
        print speed
        valuedict["properties"]["speed"] = speed
        valuedict["properties"]["duration"] = duration
        featurelist.append(valuedict)
    results["features"] = featurelist
    with open (jsondestination,'w')as outfile:
        json.dump(results,outfile)
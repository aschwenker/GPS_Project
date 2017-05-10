import json
import numpy as np
import pandas as pd
import os
import cherrypy
import csv
import shutil
import gzip
import math
import tempfile
from collections import deque, Counter
import uuid
directory_name = tempfile.mkdtemp()


config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8
  }
}



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
    
    
def gpsroute():
    """Takes in the gps data as a list, reads it and enriches it.
    then returns a geojson feature collection of line segments between each lat,lon given"""

    results ={"type":"FeatureCollection","features":[]}
    x={}
    featurelist = []
    lonlatlist = []
    latlonlist = []
    for x in os.listdir(directory_name):
        path = os.path.join(directory_name, x)
        print path
        with open(path,'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print row
                lonlatlist.append([row['Longitude'],row['Latitude'],row['ActivityDateTimeEST']])
                #lat, lon, odometer
    lonlatlist =sorted(lonlatlist, key=lambda x: x[2])
    #sorts on odometer
    for listlon in lonlatlist:
        latlon=((float(listlon[0]),float(listlon[1])))
        #tuple
        time = listlon[2]
        appenditem=(latlon,time)
        latlonlist.append(appenditem)
        #list of ((lat,lon),time)
    
    lonLatLength = len(latlonlist)
    print lonLatLength
    for i in range(1,lonLatLength-1):
        valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":"","mean_speed":"","duration":""} }
        a = i
        b = i + 1
        x=latlonlist[a][0],latlonlist[b][0]
        distance = haversine_np(x)
        time = latlonlist[b][1]-latlonlist[a][1]
        if time > 0:
            speed = float(distance)/float(time)
            z=(x,speed)
        else:
            continue
        if i >3:
            meanseqstart =i-2
            print meanseqstart
            meanseq = meanseqstart+4
            piece = latlonlist[meanseqstart:meanseq]
            seq=[]
            for i in range (0,len(piece)):
                one = piece[i][1]
                print one
                seq.append(one)
            print seq
            seqSize = len(seq)
            d=deque(seq[0:seqSize])
            mean_speed = np.mean(d)
        else:
            mean_speed = speed

        valuedict["geometry"]["coordinates"] =x
        valuedict["properties"]["distance"] = distance
        valuedict["properties"]["mean_speed"] = mean_speed
        valuedict["properties"]["duration"] = time
        featurelist.append(valuedict)
    results["features"] = featurelist

    with open (jsondestination,'w')as outfile:
        json.dump(results,outfile)

class App:
    jsonfilename = str(uuid.uuid4())
    jsondestination = os.path.join(directory_name, jsonfilename)
    @cherrypy.expose
    def index(self):
        """loads the index file"""
        return file('C:/Users/ASchwenker/Documents/GitHub/GPS_Project/index.html')
        
    @cherrypy.expose
    def upload(self):
        """uploads csv from request, creates 
        list of data and calls gsproute to return geojson"""
        filename    = str(uuid.uuid4())
        destination = os.path.join(directory_name, filename)
        with open(destination, 'wb') as f:
            shutil.copyfileobj(cherrypy.request.body, f)
    
    @cherrypy.expose
    def geo(self):
        gpsroute()
        """used as a static geojson sample to test html geojson link load worked"""
        return file(jsondestination)

        

#gpsroute(csv)
if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', config)

#os.removedirs(directory_name)
        




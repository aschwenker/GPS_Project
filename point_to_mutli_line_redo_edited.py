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
from datetime import datetime
directory_name = tempfile.mkdtemp()


config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
    'server.environment' : "production",
    'engine.autoreload_on' : True,
    'engine.autoreload_frequency' : 60
  }
}

def writer(filename):
    destination = os.path.join(directory_name, filename)
    with open(destination, 'wb') as f:
        shutil.copyfileobj(cherrypy.request.body, f)


def isTimeFormat(input):
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
    
    
def gpsroute(filename,destination):
    """Takes in the gps data as a list, reads it and enriches it.
    then returns a geojson feature collection of line segments between each lat,lon given"""

    results ={"type":"FeatureCollection","features":[]}
    x={}
    featurelist = []
    lonlatlist = []
    latlonlist = []
    timeheader = ''
    path = os.path.join(directory_name, filename)
    with open(path,'r') as csvfile:
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
    with open(path,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            timeraw=row[timeheader]
            print timeraw
            if isTimeFormat(timeraw):       
                time = datetime.strptime(timeraw,"%m/%d/%Y %H:%M:%S")
                print time
                lonlatlist.append([[row[lonheader],row[latheader]],time])
            else:
                time = datetime.strptime(timeraw,"%m/%d/%Y %H:%M")
                lonlatlist.append([[row[lonheader],row[latheader]],time])
            #appends to a list to the list: [(lat, lon ),time]
            
            #lat, lon, time
    print lonlatlist
    lonlatlist =sorted(lonlatlist, key=lambda x: x[1])
    #sorts on time
    for listlon in lonlatlist:
        latlon=((float(listlon[0][0]),float(listlon[0][1])))
        #tuple
        time = listlon[1]
        appenditem=([latlon,time])
        latlonlist.append(appenditem)
        #list of ((lat,lon),time)
    
    lonLatLength = len(latlonlist)
    for i in range(0,lonLatLength-1):
        #creates dictionary that will populate feature list of dict created above
        valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":"","speed":"","duration":""} }
        a = i
        b = i + 1
        x=latlonlist[a][0],latlonlist[b][0]
        distance = round(haversine_np(x),2)
        time = latlonlist[b][1]-latlonlist[a][1]
        duration = time.seconds
        duration = (duration/60)
        if duration > 0:
            speed = round((float(distance)/float(duration)),2)
        else:
            speed = 0
        x=latlonlist[a][0],latlonlist[b][0]
        valuedict["geometry"]["coordinates"] =x
        valuedict["properties"]["distance"] = distance
        valuedict["properties"]["speed"] = speed
        valuedict["properties"]["duration"] = duration
        featurelist.append(valuedict)
        print featurelist
    results["features"] = featurelist

    with open (destination,'w')as outfile:
        json.dump(results,outfile)

class App:
    filename    = str(uuid.uuid4())
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
        writer(self.filename)

    @cherrypy.expose
    def userinput(self,unique):    
        """user provides unique string to access their db data"""
    @cherrypy.expose
    def geo(self):
        gpsroute(self.filename,self.jsondestination)
        """used as a static geojson sample to test html geojson link load worked"""
        return file(self.jsondestination)

        

#gpsroute(csv)
if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', config)

#os.removedirs(directory_name)
        




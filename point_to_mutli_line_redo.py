import json
import numpy as np
import pandas as pd
import os
import cherrypy
import csv
import shutil
import gzip
import math

config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
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
    
def gpsroute(file_content):
    uploadlist=[]
    uploadlist = file_content.split('\n') 
    results ={"type":"FeatureCollection","features":[]}
    x={}
    featurelist = []
    lonlatlist = []
    latlonlist = [] 
    xlist=[x for x in range(1,len(uploadlist))]
    for x in xlist:
        row =uploadlist[x]
        row = row.split(",")
        #print row
        #print type(row)
        lonlatlist.append([row[1],row[2],row[25]])
        #print lonlatlist
    lonlatlist =sorted(lonlatlist, key=lambda x: x[2])
    for listlon in lonlatlist:
        latlon=((listlon[0],listlon[1]))
        latlonlist.append(latlon)
    
    lonLatLength = len(latlonlist)
    for i in range(1,lonLatLength-1):
        valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":""} }
        a = i
        b = i + 1
        x=latlonlist[a],latlonlist[b]
        print x
        latinput =x[0][0]
        print latinput
        print type(latinput)
        longlatinput = float(latinput)
        print type(longlatinput)
        distance = haversine_np(x)
        print distance
        valuedict["geometry"]["coordinates"] =x
        valuedict["properties"]["distance"] = distance
        featurelist.append(valuedict)
    results["features"] = featurelist
    geojson = json.dumps(results)
    return geojson

        
    
class App:
    @cherrypy.expose
    def index(self):
        return file('C:/Users/ASchwenker/Documents/GitHub/GPS_Project/index.html')
    @cherrypy.expose
    def upload(self):
        '''Handle non-multipart upload'''
        upload = cherrypy.request.body.read()
        return upload
    
    @cherrypy.expose
    def geojson(self):
        return gpsroute(self.upload())

        #with gzip.open(upload,'r') as f:
        #    file_content=f.read()
        #print type(file_content)
        #with open(destination, 'wb') as f:
        #    shutil.copyfileobj(cherrypy.request.body, f)
            

    
        

#gpsroute(csv)
if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', config)
        

#gpsroute()


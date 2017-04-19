import json
import numpy as np
import pandas as pd
import os
import cherrypy
import csv
import shutil
import gzip
import math
from collections import deque, Counter
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
    
def gpsroute(uploadlist):
    #uploadlist=[]
    #uploadlist = file_content.split('\n') 
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
        time = float(listlon[2])
        appenditem=(latlon,time)
        latlonlist.append(appenditem)
    
    lonLatLength = len(latlonlist)
    print lonLatLength
    for i in range(1,lonLatLength-1):
        valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":"","mean_speed":"","duration":""} }
        a = i
        b = i + 1
        x=latlonlist[a][0],latlonlist[b][0]
        distance = haversine_np(x)
        time = float(latlonlist[b][1])-float(latlonlist[a][1])
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
            mean_speed = [np.mean(d)]
        else:
            mean_speed = speed

        valuedict["geometry"]["coordinates"] =x
        valuedict["properties"]["distance"] = distance
        valuedict["properties"]["mean_speed"] = mean_speed
        valuedict["properties"]["duration"] = time
        featurelist.append(valuedict)
    results["features"] = featurelist
    return (json.dumps(results))

        
    
class App:
    @cherrypy.expose
    def index(self):
        return file('C:/Users/ASchwenker/Documents/GitHub/GPS_Project/index.html')
    @cherrypy.expose
    def geo(self):
        return file('C:/Users/ASchwenker/Documents/GitHub/GPS_Project/apriltest.geojson')
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self):
        upload = cherrypy.request.body.read()
        print type(upload)
        uploadlist=[]
        uploadlist = upload.split('\n')

        return gpsroute(uploadlist)

    
    """@cherrypy.expose
    def gpsroute(self):
        upload = cherrypy.request.body.read()
        #return upload
        #upload = self.upload()
        print upload
        uploadlist=[]
        uploadlist = upload.split('\n')
        
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
            latinput =x[0][0]
            longlatinput = float(latinput)
            distance = haversine_np(x)
            valuedict["geometry"]["coordinates"] =x
            valuedict["properties"]["distance"] = distance
            featurelist.append(valuedict)
        results["features"] = featurelist
        geojson = json.dumps(results)
        print geojson"""
        

    
        

#gpsroute(csv)
if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', config)
        

#gpsroute()


import json
import numpy as np
import pandas as pd
import os
import cherrypy

import shutil

config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
  }
}


def gpsroute(csv):

        

    results ={"type":"FeatureCollection","features":[]}
    x={}
    featurelist = []
    lonlatlist = []
    latlonlist = []
    with open(csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lonlatlist.append([float(row[0]),float(row[1]),float(row[2])])
        lonlatlist =sorted(lonlatlist, key=lambda x: x[2])
        for listlon in lonlatlist:
            latlon=((listlon[0],listlon[1]))
        latlonlist.append(latlon)
        print lonlatlist
    
    lonLatLength = len(latlonlist)
    for i in range(1,lonLatLength-1):
        valuedict = {"type": "Feature","geometry":{"type" : "LineString","coordinates":[]},"properties":{"distance":""} }
        a = i
        b = i + 1
        x=latlonlist[a],latlonlist[b]
        distance = haversine_np(x)
        valuedict["geometry"]["coordinates"] =x
        valuedict["properties"]["distance"] = distance
        featurelist.append(valuedict)
    results["features"] = featurelist
    print json.dumps(results)


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
    
    
class App:
    @cherrypy.expose
    def index(self):
        return file('H:/CLASS/GTECH734/testuploader/index.html')
    @cherrypy.expose
    def upload(self):
        '''Handle non-multipart upload'''

        filename    = os.path.basename(cherrypy.request.headers['x-filename'])
        destination = os.path.join('/Users/ASchwenker/Desktop', filename)
        with open(destination, 'wb') as f:
            shutil.copyfileobj(cherrypy.request.body, f)
        


if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', config)
        

#gpsroute()


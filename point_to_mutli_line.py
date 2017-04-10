import psycopg2
import json
import numpy as np
import pandas as pd
import os, os.path
import cherrypy
from cherrypy.process import  plugins
path = os.getcwd()
print path
#class gpsroute(object):
    #@cherrypy.expose
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


"""class MagicBoxInterface(object):

    @cherrypy.expose
    def index(self):
        return file('index.html')
        print "file returned"

    @cherrypy.expose
    def uploadSound(self,  cardID='', myFile=None):
        print 'uploadSound : ',  cardID
        print 'uploadSound : ',  myFile
        return ''"""

class Root(object):

    @cherrypy.expose
    def index(self):
        return file('C:\Users\ASchwenker\Documents\GitHub\GPS_Project\index.html')
    @cherrypy.expose
    def upload(self, ufile):
        upload_path = os.path.normpath('C:\Users\ASchwenker\Documents\GitHub\GPS_Project')
        upload_file = os.path.join(upload_path, ufile.filename)
        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = ufile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        out = '''
           length: {}
           filename: {}
           mime-type: {}
              ''' .format(size, ufile.filename, ufile.content_type, data)
        return out

#gpsroute()
cherrypy.quickstart(Root(), '/')
#cherrypy.quickstart(gpsroute(),'/')

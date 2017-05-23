import shutil
import os
import csv
import json
import uuid
import tempfile
import cherrypy
import numpy as np
import psycopg2 as pg
import config as conf
from datetime import datetime
from math import radians, cos, sin, asin, sqrt

def writer(csvdestination):
    with open(csvdestination, 'wb') as f:
        shutil.copyfileobj(cherrypy.request.body, f)
            
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

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


def gpsroute(csvdestination, jsondestination):
    """Takes in the gps data as a list, reads it and enriches it.
    then returns a geojson feature collection of line segments between each lat,lon given"""

    results = {"type": "FeatureCollection", "features": []}
    x = {}
    featurelist = []
    lonlatlist = []
    latlonlist = []
    timeheader = ''
    with open(csvdestination, 'r') as csvfile:
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
    with open(csvdestination, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            timeraw = row[timeheader]
            if isTimeFormat(timeraw):
                time = datetime.strptime(timeraw, "%m/%d/%Y %H:%M:%S")
                lonlatlist.append([[row[lonheader], row[latheader]], time])
            else:
                time = datetime.strptime(timeraw, "%m/%d/%Y %H:%M")
                lonlatlist.append([[row[lonheader], row[latheader]], time])
                # appends to a list to the list: [[lat, lon ],time]
                # necessary becuase couldnt perform following sort if it were a tuple
    lonlatlist = sorted(lonlatlist, key=lambda x: x[1])
    # sorts on time
    for listlon in lonlatlist:
        latlon = ((float(listlon[0][0]), float(listlon[0][1])))
        # tuple
        time = listlon[1]
        appenditem = ([latlon, time])
        # restructuring format
        latlonlist.append(appenditem)
        # list of ((lat,lon),time)

    for i in range(0, len(latlonlist) - 1):
        # must be range(len-1) to accomodate line segment lat/lon pairs
        valuedict = {"type": "Feature", "geometry": {"type": "LineString", "coordinates": []},
                     "properties": {"distance": "", "speed": "", "duration": ""}}
        # creates dictionary that will populate feature list of dict created above
        x = latlonlist[i][0], latlonlist[i + 1][0]
        # ((lon,lat),(lon,lat)) (tuple,tuple) represents start & end of line seg
        distance = round(haversine_np(x), 2)
        time = latlonlist[i + 1][1] - latlonlist[i][1]
        # start and end time for seg
        print (float(time.seconds))
        duration = ((float(time.seconds)) / 3600)
        # converts to hours
        print duration
        if float(duration) > 0:
            print float(distance), "/", float(duration)
            speed = round((float(distance) / float(duration)), 2)
        else:
            speed = 0
        x = latlonlist[i][0], latlonlist[i + 1][0]
        valuedict["geometry"]["coordinates"] = x
        valuedict["properties"]["distance"] = distance
        print speed
        valuedict["properties"]["speed"] = speed
        valuedict["properties"]["duration"] = duration
        featurelist.append(valuedict)
    results["features"] = featurelist
    with open(jsondestination, 'w')as outfile:
        json.dump(results, outfile)


# functions required:
def RollingWindow(seq, seqSize, winSize, cal):
    # modules used
    from collections import deque
    from itertools import islice
    import numpy as np

    """
     Purpose: Find the mean or variance for the points in a sliding window (fixed size)
              as it is moved from left to right by one point at a time.
      Inputs:
          seq -- list containing items for which a mean (in a sliding window) is
                 to be calculated (N items)
            N -- length of sequence
            M -- number of items in sliding window
      Otputs:
        vals -- list of means or variance for seq
    """
    # Load deque (d) with first window of seq
    d = deque(seq[0:winSize])
    if cal == 'v':
        vals = [np.var(d)]  # contains variance of first window
    else:
        vals = [np.mean(d)]  # contains mean of first window

    # Now slide the window by one point to the right for each new position (each pass through
    # the loop). Stop when the item in the right end of the deque contains the last item in seq
    if cal == 'v':
        for item in islice(seq, winSize, seqSize):
            old = d.popleft()  # pop oldest from left
            d.append(item)  # push newest in from right
            vals.append(np.var(d))
    else:
        for item in islice(seq, winSize, seqSize):
            old = d.popleft()  # pop oldest from left
            d.append(item)  # push newest in from right
            vals.append(np.mean(d))

    # add buffer values for start of the seq
    buff = winSize / 2 - 1
    while buff > 0:
        vals.insert(0, vals[0])
        buff -= 1

    # add buffer values for end of the seq
    buff = winSize / 2
    while buff > 0:
        vals.append(vals[-1])
        buff -= 1

    return vals


# Calculate time interval between two points'
def TimeInterval(time):

    TIME_INTERVAL = []
    for x in xrange(len(time)):
        difference = (time[x] - time[x-1])
        TIME_INTERVAL.append((difference.days *86400.0 + difference.seconds)/1.0)
    TIME_INTERVAL[0] =  TIME_INTERVAL[1]
    return TIME_INTERVAL


# Calculate distance between two points
def Haversine(lon,lat):

    # Calculate distance between two points (Haversine formula)'
    Distance = []
    for x in xrange(len(lon)):
        lon1 = lon[x]
        lon2 = lon[x-1]
        lat1 = lat[x]
        lat2 = lat[x-1]

        # convert decimal degrees to
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
        c = 2.0 * asin(sqrt(a))
        km = 6367.0 * c
        meters = km * 1000.0
        Distance.append(meters)
    Distance[0] =  Distance[1]
    return Distance

# Calculate speed for point
def SpeedCal(distance,time):
    speed = []
    for x in xrange(len(time)):
        if time[x] > 0:
            speed.append((distance[x] / time[x]))  # (.444M/s equivalent of 1.6 KM/Hour)
        else:
            speed.append(0.0)  # this should not happen
    speed[0] = 0.0
    return speed


def MagAccelCal(accelx, accely, accelz):
    moa = []
    for x in xrange(len(accelx)):
        sumsq = accelx[x]** 2 + accely[x]** 2 + accelz[x]** 2
        moa.append(sqrt(sumsq))
    return moa


def ProcessMobileData(name):
    # fetch data from mobile db
    name = 'lsava7'
    cnxn = pg.connect(host=conf.db["host"], database=conf.db["database"], user=conf.db["user"],
                      password=conf.db["password"])
    cursor = cnxn.cursor()

    try:
        sql = "SELECT lon,lat,time,accelx,accely,accelz FROM mobiledb WHERE userid = '{0}' ".format(name)
        cursor.execute(sql)
        data = cursor.fetchall()


        # lists to store feed data
        _lon = []
        _lat = []
        _time = []
        _accelx = []
        _accely = []
        _accelz = []

        # Populate the respective lists with the GPS coordinates, xyz readings, and time data
        for x in xrange(len(data)):
            _lon.append(float(data[x][0]))
            _lat.append(float(data[x][1]))
            _time.append(datetime.strptime((data[x][2])[:-3], "%Y-%m-%d %H:%M:%S"))
            _accelx.append(float(data[x][3]))  # x values
            _accely.append(float(data[x][4]))  # y values
            _accelz.append(float(data[x][5]))  # z values

        # lists to store calculation
        _distance = Haversine(_lon, _lat)
        _timeInterval = TimeInterval(_time)
        _speed = SpeedCal(_distance, _timeInterval)
        _magAccel = MagAccelCal(_accelx, _accely, _accelz)

        # smooth values with rolling windows
        _avgSpeed = RollingWindow(_speed, len(_speed), 12, 'm')  # uses 1 min of context
        _magAccel = RollingWindow(_magAccel, len(_speed), 12, 'v')  # uses 1 min of context

    finally:
        cursor.close()
        cnxn.close()

    return _lat,_lon, _distance, _avgSpeed, _magAccel


def ReturnGeoJSON(data):

    # create geojson for mobile data
    _featureCollection = {"type": "FeatureCollection",
                          "features": []}

    _feature = {"type": "Feature",
                "geometry": {"type": "LineString", "coordinates": []},
                "properties": {"distance": "", "speed": "", "activity metric": ""}}

    # assign mobile data to geojson
    _featureslist = []
    for x in xrange(1,len(data[0])):
        _feature = {"type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": []},
                    "properties": {"distance": "", "speed": "", "activity metric": ""}}
        val =[data[1][x-1], data[0][x-1]],[data[1][x], data[0][x]]
        _feature["geometry"]["coordinates"] = val #_lat, _lon
        _feature["properties"]["distance"] =  data[2][x]          #_distance
        _feature["properties"]["speed"] =     data[3][x]         #_avgSpeed
        _feature["properties"]["activity metric"] = data[4][x]    #_magAccel
        _featureslist.insert(x,_feature)
        del _feature
    _featureCollection["features"] = _featureslist

    # create output file for geojson
    _directory = tempfile.mkdtemp()
    _jsonfilename = str(uuid.uuid4())
    _jsondestination = os.path.join(_directory, _jsonfilename)

    with open(_jsondestination, 'w')as _outputfile:
        json.dump(_featureCollection, _outputfile)
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    return  _featureCollection

    return json.dumps(ReturnGeoJSON(data))




if __name__ == '__main__':


    # fetch data from mobile db
    name = 'lsava7'
    cnxn = pg.connect(host=conf.db["host"], database=conf.db["database"], user=conf.db["user"],
                      password=conf.db["password"])
    cursor = cnxn.cursor()

    try:
        sql = "SELECT lon,lat,time,accelx,accely,accelz FROM mobiledb WHERE userid = '{0}' ".format(name)
        cursor.execute(sql)
        data = cursor.fetchall()

    finally:
        cursor.close()
        cnxn.close()

    # lists to store feed data
    _lon = []
    _lat = []
    _time = []
    _accelx = []
    _accely = []
    _accelz = []

    # Populate the respective lists with the GPS coordinates, xyz readings, and time data
    for x in xrange(len(data)):
        _lon.append(float(data[x][0]))
        _lat.append(float(data[x][1]))
        _time.append(datetime.strptime((data[x][2])[:-3], "%Y-%m-%d %H:%M:%S"))
        _accelx.append(float(data[x][3]))  # x values
        _accely.append(float(data[x][4]))  # y values
        _accelz.append(float(data[x][5]))  # z values


    # lists to store calculation
    _distance = Haversine(_lon,_lat)
    _timeInterval= TimeInterval(_time)
    _speed = SpeedCal(_distance,_timeInterval)
    _magAccel = MagAccelCal(_accelx, _accely, _accelz)

    # smooth values with rolling windows
    _avgSpeed = RollingWindow(_speed, len(_speed),12,'m') # uses 1 min of context
    _magAccel=  RollingWindow( _magAccel, len(_speed),12,'v') # uses 1 min of context



    #make json of features
    _featureCollection = {"type": "FeatureCollection",
                          "features": []}

    _feature = {"type": "Feature",
                "geometry":{"type" : "LineString","coordinates":[]},
                "properties":{"distance":"","speed":"","activity metric":""}}

    _featuresList =[]
    for x in xrange(len(data)-1):
        #val = [_lat[x],_lon[x]],[_lat[x+1], _lon[x+1]]
        _feature["geometry"]["coordinates"] =[_lat[x],_lon[x]],[_lat[x+1], _lon[x+1]]  #val
        _feature["properties"]["distance"] = _distance[x]
        _feature["properties"]["speed"] = _avgSpeed[x]
        _feature["properties"]["activity metric"] = _magAccel[x]
        _featuresList.append(_feature)
        _featureCollection["features"] =_featuresList

    _directory = tempfile.mkdtemp()
    _jsonFilename = str(uuid.uuid4())
    _jsonDestination = os.path.join(_directory, _jsonFilename)


    with open(_jsonDestination, 'w')as outfile:
        json.dump( _featureCollection, outfile)


    #function calls
    data =ProcessMobileData('lsava7')
    outputfile =ReturnGeoJSON(data)


    # class App:
    #
    #     name =''
    #     @cherrypy.expose
    #     def index(self):
    #         """loads the index file"""
    #         return file('C:\Users\carsi\Desktop\sample_data\index.html')
    #
    #     @cherrypy.expose
    #     def generate(self,name):
    #         data = ProcessMobileData(str(name))
    # cherrypy.quickstart(App(), '/', conf.config)

    print"done"



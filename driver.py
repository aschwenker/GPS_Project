import json
import uuid
import tempfile
import os
import datetime
import psycopg2  as pg
import config as conf
from math import radians, cos, sin, asin, sqrt


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
            speed.append(distance[x] / time[x])  # (.444M/s equivalent of 1.6 KM/Hour)
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
            _time.append(datetime.datetime.strptime((data[x][2])[:-3], "%Y-%m-%d %H:%M:%S"))
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
    _feature["geometry"]["coordinates"] = data[0], data[1] #_lat, _lon
    _feature["properties"]["distance"] =  data[2]          #_distance
    _feature["properties"]["speed"] =     data[3]          #_avgSpeed
    _feature["properties"]["activity metric"] = data[4]    #_magAccel
    _featureCollection["features"] = _feature

    # create output file for geojson
    directory_name = tempfile.mkdtemp()
    filename = str(uuid.uuid4())
    jsonfilename = str(uuid.uuid4())
    jsondestination = os.path.join(directory_name, jsonfilename)

    with open(jsondestination, 'w')as outputfile:
        json.dump(_featureCollection, outfile)

    return outputfile

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
        _time.append(datetime.datetime.strptime((data[x][2])[:-3], "%Y-%m-%d %H:%M:%S"))
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


    # for x in xrange(len(data)):
        #x = latlonlist[a][0], latlonlist[b][0]
        #k =_lat[x],_lon[x]
    _feature["geometry"]["coordinates"] = _lat, _lon
    _feature["properties"]["distance"] = _distance
    _feature["properties"]["speed"] = _avgSpeed
    _feature["properties"]["activity metric"] = _magAccel
    _featureCollection["features"] = _feature

    directory_name = tempfile.mkdtemp()
    filename = str(uuid.uuid4())
    jsonfilename = str(uuid.uuid4())
    jsondestination = os.path.join(directory_name, jsonfilename)


    with open(jsondestination, 'w')as outfile:
        json.dump( _featureCollection, outfile)


    #function calls
    data =ProcessMobileData(name)
    outputfile =ReturnGeoJSON(data)


    print"results"



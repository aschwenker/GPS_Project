import csv
import datetime
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


if __name__ == '__main__':

    # file location
    dfile = 'C:\Users\carsi\Desktop\sample_data\lsava7Data.csv'

    # Open data and read into a 2-D list
    with open(dfile) as d:
        reader = csv.reader(d)
        data = list(reader)


    # lists to store feed data
    #_pid =[]
    _lon = []
    _lat = []
    _time = []
    _accelx = []
    _accely = []
    _accelz = []


    # Populate the respective lists with the squared xyz values and time data
    for x in xrange(len(data)):
        if data[x][1] == 'pid':
            pass
        else:
            _lon.append(float(data[x][2]))
            _lat.append(float(data[x][3]))
            _time.append(datetime.datetime.strptime(str(data[x][5]), "%Y-%m-%d %H:%M:%S"))
            _accelx.append(float(data[x][11]))  # x values
            _accely.append(float(data[x][12]))  # y values
            _accelz.append(float(data[x][13]))  # z values

    #_pid = xrange(len(_lon))

    # lists to store calculation
    _distance = Haversine(_lon,_lat)
    _timeInterval= TimeInterval(_time)
    _speed = SpeedCal(_distance,_timeInterval)
    _magAccel = MagAccelCal(_accelx, _accely, _accelz)

    print '# smoothing of values'
    avgspeed = RollingWindow(_speed, len(_speed),24,'m') # uses 2 min of context
    magAccel=  RollingWindow( _magAccel, len(_speed),24,'v') # uses 2 min of context

    print "burr"


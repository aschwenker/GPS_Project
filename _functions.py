import numpy as np
import pandas as pd


def RunningMean(seq, seqSize, winSize):
    # modules and functions used
    from collections import deque, Counter
    from itertools import islice
    import numpy as np
    from pdb import set_trace
    """
     Purpose: Find the mean for the points in a sliding window (fixed size)
              as it is moved from left to right by one point at a time.
      Inputs:
          seq -- list containing items for which a mean (in a sliding window) is
                 to be calculated (N items)
            N -- length of sequence
            M -- number of items in sliding window
      Otputs:
        means -- list of means with size N - M + 1

    """
    # Load deque (d) with first window of seq
    d = deque(seq[0:winSize])
    means = [np.mean(d)]  # contains mean of first window
    # Now slide the window by one point to the right for each new position (each pass through
    # the loop). Stop when the item in the right end of the deque contains the last item in seq
    for item in islice(seq, winSize, seqSize):
        old = d.popleft()  # pop oldest from left
        d.append(item)  # push newest in from right
        means.append(np.mean(d))  # mean for current window

    buff = winSize / 2 - 1
    while buff > 0:
        means.insert(0, means[0])
        # print buff
        buff -= 1

        # add/ buffer values at end of the seq
    buff = winSize / 2
    while buff > 0:
        means.append(means[-1])
        buff -= 1
    return means


def TimeInterval(time):

    # Calculate time interval between two points')
    TIME_INTERVAL = []
    for x in xrange(len(time)):
        difference = (time[x] - time[x-1])
        TIME_INTERVAL.append((difference.days *86400.0 + difference.seconds)/1.0)
    TIME_INTERVAL[0] =  TIME_INTERVAL[1]
    return TIME_INTERVAL


def Haversine(lon,lat):

    # Calculate distance between two points (Haversine formula)'
    Distance = []
    for x in xrange(len(lon)):
        lon1 = lon[x]
        lon2 = lon[x-1]
        lat1 = lat[x]
        lat2 = lat[x-1]

        # convert decimal degrees to
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
        c = 2.0 * asin(sqrt(a))
        km = 6367.0 * c
        meters = km * 1000.0
        Distance.append(meters)
    Distance[0] =  Distance[1]


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

lon1, lon2, lat1, lat2 = np.random.randn(4, 1000000)
print lon1, lon2, lat1, lat2
df = pd.DataFrame(data={'lon1':lon1,'lon2':lon2,'lat1':lat1,'lat2':lat2})
km = haversine_np(df['lon1'],df['lat1'],df['lon2'],df['lat2'])
print type(km)
alt = haversine_np(-74.00594, -122.41942, 40.71278, 37.77493)
print alt

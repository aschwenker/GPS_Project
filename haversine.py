import numpy as np
import pandas as pd


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

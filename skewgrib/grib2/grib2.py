from typing import List, Any

import pygrib
import numpy as np
from metpy.units import units
import pathlib

# https://nomads.ncep.noaa.gov/pub/data/nccf/com/rap/prod/rap.20201213/rap.t00z.awp130bgrbf00.grib2
file = str(pathlib.Path(__file__).parent) + '/../../files/rap.t00z.awp130bgrbf00.grib2'
grb_index = pygrib.index(file, 'name', 'typeOfLevel')

# create helper function to enumerate and return data types
def helper_return_data_types():
    grb_messages = []
    for grb in pygrib.open(file):
        grb_messages.append(grb)

    return grb_messages

def return_data(type_of_data, location):
    tolerance = 0.1

    airports = {
        'VNY':
            { 'lat': 34.2096, 'lon': -118.4896 }
    }

    lat, lon = airports[location]['lat'], airports[location]['lon']

    selected_grbs = grb_index.select(name=type_of_data, typeOfLevel='hybrid')

    returned_data = []
    for grb in selected_grbs:
        data = grb.data(lat1=lat-tolerance,lat2=lat+tolerance,
                        lon1=lon-tolerance,lon2=lon+tolerance)
        returned_data.append(data[0][0])

    return (returned_data * getattr(units, selected_grbs[0].units))
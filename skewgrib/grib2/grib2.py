from typing import List, Any

import pygrib
import numpy as np
from metpy.units import units

# https://nomads.ncep.noaa.gov/pub/data/nccf/com/rap/prod/rap.20201213/rap.t00z.awp130bgrbf00.grib2
grb_index = pygrib.index('../files/rap.t00z.awp130bgrbf00.grib2', 'name', 'typeOfLevel')

# todo: create helper function to enumerate and return data types

def return_data(type_of_data, location, type_of_units):
    tolerance = 0.1

    airports = {
        'VNY':
            { 'lat': 34.2096, 'lon': -118.4896 }
    }

    # VNY
    lat, lon = airports[location]['lat'], airports[location]['lon']

    # grbs = pygrib.open('../files/rap.t00z.awp130bgrbf00.grib2')
    #
    # grb_values = []
    #
    # for grb in grbs:
    #     grb_values.append(grb)
    #
    # grb = grbs.message(1)
    # keys = grb.keys()
    # data, units, level, typeOfLevel = grb.data(lat1=lat-tolerance,lat2=lat+tolerance,
    #                                            lon1=lon-tolerance,lon2=lon+tolerance), grb.units, grb.typeOfLevel, grb.level

    selected_grbs = grb_index.select(name=type_of_data, typeOfLevel='hybrid')

    returned_data: List[Any] = []
    for grb in selected_grbs:
        data = grb.data(lat1=lat-tolerance,lat2=lat+tolerance,
                        lon1=lon-tolerance,lon2=lon+tolerance)
        returned_data.append(data[0][0])

    return np.array(returned_data, np.float64) * type_of_units

p = return_data('Pressure', 'VNY', units.hPa)
T = return_data('Temperature', 'VNY', units.degC)
# todo: need to find representative data name
# Td = return_data('Dewpoint', 'VNY', units.degC)
# todo
# wind_speed = df['speed'].values * units.knots
# todo
# wind_dir = df['direction'].values * units.degrees
# todo: figure out what this does
# u, v = mpcalc.wind_components(wind_speed, wind_dir)

print("break")
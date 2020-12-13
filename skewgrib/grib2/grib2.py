import pygrib
from metpy.units import units

def return_temp():
    # VNY
    lat, lon, tolerance = 34.2096, -118.4896, 0.1

    grb_index = pygrib.index('../files/rap.t00z.awp130pgrbf00.grib2', 'name', 'typeOfLevel')
    selected_grbs = grb_index.select(name='Temperature',typeOfLevel='isobaricInhPa')

    # Surface-level
    grb = selected_grbs[36]
    data, lats, lons = grb.data(lat1=lat-tolerance,lat2=lat+tolerance,
                                 lon1=lon-tolerance,lon2=lon+tolerance)
    # First index is min value
    t=((data[0] * units.kelvin).to(units.degC))
    print(t)
    return t

return_temp()
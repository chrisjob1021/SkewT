import matplotlib.pyplot as plt
import numpy as np

import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units

from skewgrib.grib2 import grib2

plt.rcParams['figure.figsize'] = (9, 9)

col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']

# https://nomads.ncep.noaa.gov/pub/data/nccf/com/rap/prod/rap.20201213/rap.t00z.awp130bgrbf00.grib2
grb = grib2.GribObject('files/rap.t00z.awp130bgrbf00.grib2')
location = 'VNY'

u = grb.return_data('U component of wind', location).to(units('m/s'))
v = grb.return_data('V component of wind', location).to(units('m/s'))
p = grb.return_data('Pressure', location).to(units.hPa)
T = grb.return_data('Temperature', location).to(units.degC)

specific_humidity = grb.return_data('Specific humidity', location)
dewpoints = []
# todo: make helper function
for i, val in enumerate(specific_humidity):
    dewpoints.append(np.float64(mpcalc.dewpoint_from_specific_humidity(val, T[i], p[i])))
Td = units.Quantity(dewpoints, units.degC)

wind_speed = []
for i, val in enumerate(v):
    wind_speed.append(np.float64(mpcalc.wind_speed(u[i], val)))
wind_speed = units.Quantity(wind_speed, units('m/s')).to(units.knots)

wind_dir = []
for i, val in enumerate(v):
    wind_dir.append(np.float64(mpcalc.wind_direction(u[i], val)))
wind_dir = units.Quantity(wind_dir, units('dimensionless')).to(units.degrees)

# Example of defining your own vertical barb spacing
skew = SkewT()

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')

# Set spacing interval--Every 50 mb from 1000 to 100 mb
my_interval = np.arange(100, 1000, 50) * units('mbar')
ix = list(range(50))

# Plot only values nearest to defined interval values
skew.plot_barbs(p[ix], u[ix], v[ix])

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
skew.ax.set_ylim(1000, 100)

# Show the plot
plt.show()

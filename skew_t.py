import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units

from skewgrib.grib2 import grib2

plt.rcParams['figure.figsize'] = (9,9)

col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']

df = pd.read_fwf(get_test_data('jan20_sounding.txt', as_file_obj=False),
                 skiprows=5, usecols=[0, 1, 2, 3, 6, 7], names=col_names)

# Drop any rows with all NaN values for T, Td, winds
df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed'
                       ), how='all').reset_index(drop=True)

# p = df['pressure'].values * units.hPa
# T = df['temperature'].values * units.degC
# todo: Td = df['dewpoint'].values * units.degC
# todo: wind_speed = df['speed'].values * units.knots
# todo: wind_dir = df['direction'].values * units.degrees
# todo: u, v = mpcalc.wind_components(wind_speed, wind_dir)

p = grib2.return_data('Pressure', 'VNY').to(units.hPa)
T = grib2.return_data('Temperature', 'VNY').to(units.degC)

specific_humidity = grib2.return_data('Specific Humidity', 'VNY')
# todo: need to find representative data name
Td = return_data('Dew Point Temperature', 'VNY').to(units.hPa)
# todo
# wind_speed = df['speed'].values * units.knots
# todo
# wind_dir = df['direction'].values * units.degrees
# todo: figure out what this does
# u, v = mpcalc.wind_components(wind_speed, wind_dir)

print("break")
exit

# Example of defining your own vertical barb spacing
skew = SkewT()

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')

# Set spacing interval--Every 50 mb from 1000 to 100 mb
my_interval = np.arange(100, 1000, 50) * units('mbar')

# Get indexes of values closest to defined interval
ix = mpcalc.resample_nn_1d(p, my_interval)

# Plot only values nearest to defined interval values
skew.plot_barbs(p[ix], u[ix], v[ix])

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
skew.ax.set_ylim(1000, 100)

# Show the plot
plt.show()










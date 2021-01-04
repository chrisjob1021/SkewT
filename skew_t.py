import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units

import json

# todo: comment this well
def helper_calc(func, unit, *args):
    results = []
    vals = list(zip(*args))
    for val in vals:
        results.append(np.float64(func(*val)))
    return units.Quantity(results, unit)

col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']

testData = True

if testData:
    import pandas as pd
    from metpy.cbook import get_test_data

    df = pd.read_fwf(get_test_data('may4_sounding.txt', as_file_obj=False),
                     skiprows=5, usecols=[0, 1, 2, 3, 6, 7], names=col_names)

    # Drop any rows with all NaN values for T, Td, winds
    df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed'
                       ), how='all').reset_index(drop=True)

    p = df['pressure'].values * units.hPa
    T = df['temperature'].values * units.degC
    Td = df['dewpoint'].values * units.degC
    wind_speed = df['speed'].values * units.knots
    wind_dir = df['direction'].values * units.degrees
    u, v = mpcalc.wind_components(wind_speed, wind_dir)
else:
    from grib2 import grib2

    # https://nomads.ncep.noaa.gov/pub/data/nccf/com/rap/prod/rap.20201213/rap.t00z.awp130bgrbf00.grib2
    grb = grib2.GribObject('files/rap.t00z.awp130bgrbf00.grib2')
    location = 'VNY'

    u = grb.return_data('U component of wind', location).to(units('m/s'))
    v = grb.return_data('V component of wind', location).to(units('m/s'))
    p = grb.return_data('Pressure', location).to(units.hPa)
    T = grb.return_data('Temperature', location).to(units.degC)
    Td = helper_calc(mpcalc.dewpoint_from_specific_humidity, units.degC, grb.return_data('Specific humidity', location), T, p)
    wind_speed = helper_calc(mpcalc.wind_speed, units('m/s'), u, v).to(units.knots)
    wind_dir = helper_calc(mpcalc.wind_direction, units('dimensionless'), u, v).to(units.degrees)

# Create a new figure. The dimensions here give a good aspect ratio
fig = plt.figure(figsize=(12, 9))

# Grid for plots
#gs = gridspec.GridSpec(3, 3)
#skew = SkewT(fig, rotation=45, subplot=gs[:, :2])
gs = gridspec.GridSpec(4, 4)
skew = SkewT(fig, rotation=45, subplot=gs[:, 1:])

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

skew.ax.set_ylim(1000, 200)
skew.ax.set_xlim(-30, 40)

with open("files/fip.json") as f:
    icing = json.loads(f.read())

levels, icing_probabilities = zip(*sorted(icing['data']['probability'].items(), key=lambda x: int(x[0])))
_, icing_severities = zip(*sorted(icing['data']['probability'].items(), key=lambda x: int(x[0])))
_, icing_sld = zip(*sorted(icing['data']['supercooledLargeDrop'].items(), key=lambda x: int(x[0])))

ax = fig.add_subplot(gs[:, 0])
bar = ax.barh(levels, icing_probabilities, align='center')
ax.set_xlabel('Icing Probability')
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_ylabel('Pressure Alt')

# Show the plot
plt.show()

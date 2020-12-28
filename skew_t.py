import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

import metpy.calc as mpcalc
from metpy.plots import Hodograph, SkewT
from metpy.units import units

def helper_calc(func, unit, *args):
    results = []
    for i, v in enumerate(args[0]):
        send = [ v ]
        for j in range(1,len(args)):
            send.append(args[j][i])

        results.append(np.float64(func(*send)))
    return units.Quantity(results, unit)

col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']

testData = False

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
fig = plt.figure(figsize=(9, 9))

# Grid for plots
gs = gridspec.GridSpec(3, 3)
skew = SkewT(fig, rotation=45, subplot=gs[:, :2])

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-30, 40)

ax = fig.add_subplot(gs[0, -1])
h = Hodograph(ax, component_range=60.)
h.add_grid(increment=20)
h.plot(u, v)

# Show the plot
plt.show()

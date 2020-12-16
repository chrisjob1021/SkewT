import pygrib
from metpy.units import units

class GribObject:
    def __init__(self, file):
        self.file = file
        self.grb_index = pygrib.index(self.file, 'name', 'typeOfLevel')

    def _open_file(self):
        return(pygrib.open(self.file))

    # create helper function to enumerate and return data types
    def helper_return_data_types(self):
        grb_messages = []
        grbs = self._open_file()
        for grb in grbs:
            grb_messages.append(grb)
        return grb_messages

    def return_data(self, type_of_data, location):
        tolerance = 0.1

        airports = {
            'VNY':
                {'lat': 34.2096, 'lon': -118.4896}
        }

        lat, lon = airports[location]['lat'], airports[location]['lon']

        """
        Searching for data within multi-field grib messages does not work using an index and is not supported by ECCODES library. 
        NCEP often puts u and v winds together in a single multi-field grib message. 
        You will get incorrect results if you try to use an index to find data in these messages. 
        Use the slower, but more robust open.select() in this case.
        
        https://jswhit.github.io/pygrib/api.html#pygrib.index
        """
        if 'component' in type_of_data:
            selected_grbs = self._open_file().select(name=type_of_data, typeOfLevel='hybrid')
        else:
            selected_grbs = self.grb_index.select(name=type_of_data, typeOfLevel='hybrid')

        returned_data = []
        for grb in selected_grbs:
            data = grb.data(lat1=lat - tolerance, lat2=lat + tolerance,
                            lon1=lon - tolerance, lon2=lon + tolerance)
            returned_data.append(data[0][0])

        return (returned_data * getattr(units, selected_grbs[0].units))

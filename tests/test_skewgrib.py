from skewgrib.grib2 import grib2
from metpy.units import units

class TestClass:
    def test_return_temp(self):
        assert grib2.return_temp() == units.Quantity(17.552667236328148, 'degree_Celsius')
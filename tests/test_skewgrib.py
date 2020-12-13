from skewgrib import skewgrib
from metpy.units import units

class TestClass:
    def test_return_temp(self):
        assert skewgrib.return_temp() == units.Quantity(17.552667236328148, 'degree_Celsius')
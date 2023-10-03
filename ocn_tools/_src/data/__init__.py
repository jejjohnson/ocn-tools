import pint_xarray
from loguru import logger


def add_units(da, units={}):
    da = da.pint.quantify(units)
    return da.pint.dequantify()

import numpy as np
import xarray as xr
from metpy.calc import lat_lon_grid_deltas
from metpy.units import units
import pint_xarray


def transform_360_to_180(coord: np.ndarray) -> np.ndarray:
    """This converts the coordinates that are bounded from
    [-180, 180] to coordinates bounded by [0, 360]

    Args:
        coord (np.ndarray): the input array of coordinates

    Returns:
        coord (np.ndarray): the output array of coordinates
    """
    return (coord + 180) % 360 - 180


def transform_180_to_360(coord: np.ndarray) -> np.ndarray:
    """This converts the coordinates that are bounded from
    [0, 360] to coordinates bounded by [-180, 180]

    Args:
        coord (np.ndarray): the input array of coordinates

    Returns:
        coord (np.ndarray): the output array of coordinates
    """
    return coord % 360


def latlon_deg2m(ds: xr.Dataset, mean: bool = True) -> xr.Dataset:
    """Converts the lat/lon coordinates from degrees to meters

    Args:
        ds (xr.Dataset): the dataset with the lat/lon variables
        mean (bool): the whether to use the mean dx/dy for each
            lat/lon coordinate (default=True)

    Returns:
        ds (xr.Dataset): the xr.Dataset with the normalized lat/lon coords
    """
    ds = ds.copy()

    lon_attrs = ds["lon"].attrs
    lat_attrs = ds["lat"].attrs

    out = lat_lon_grid_deltas(ds.lon * units.degree, ds.lat * units.degree)

    dx = out[0][:, 0]
    dy = out[1][0, :]

    num_dx = len(dx)
    num_dy = len(dy)

    if mean:
        lat = np.arange(0, num_dx) * np.mean(dx)
        lon = np.arange(0, num_dy) * np.mean(dy)
    else:
        dx0, dy0 = dx[0], dy[0]
        lat = np.cumsum(dx) - dx0
        lon = np.cumsum(dy) - dy0

    lon_attrs.pop("units", None)
    lat_attrs.pop("units", None)

    ds["lon"] = lon
    ds["lat"] = lat
    ds["lon"].attrs = lon_attrs
    ds["lat"].attrs = lat_attrs

    ds = ds.pint.quantify({"lon": "meter", "lat": "meter"}).pint.dequantify()
    return ds

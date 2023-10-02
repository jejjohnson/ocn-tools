import numpy as np
from ocn_tools._src.metrics.power_spectrum import (
    psd_spacetime, psd_isotropic,
    psd_isotropic_error, psd_spacetime_error,
    psd_isotropic_score, psd_spacetime_score
)
from ocn_tools._src.geoprocessing.test_geostrophic import get_ssh_data
from metpy.units import units

RNG = np.random.RandomState(123)

def test_psd_isotropic():
    
    ds = get_ssh_data()
    
    ds_psd = psd_isotropic(ds, "ssh", ["lat", "lon"])
    dims = set(["freq_r", "time"])
    assert dims == set(ds_psd.dims.keys())
    
    ds_psd = psd_isotropic(ds, "ssh", ["time", "lon"])
    dims = set(["freq_r", "lat"])
    assert dims == set(ds_psd.dims.keys())
    
    ds_psd = psd_isotropic(ds, "ssh", ["time", "lat"])
    dims = set(["freq_r", "lon"])
    assert dims == set(ds_psd.dims.keys())
    
    
def test_psd_spacetime():
    
    ds = get_ssh_data()
    
    # CASES
    ds_psd = psd_spacetime(ds, "ssh", ["time",])
    dims = set(["freq_time", "lat", "lon"])
    assert dims == set(ds_psd.dims.keys())
    
    ds_psd = psd_spacetime(ds, "ssh", ["lon"])
    dims = set(["time", "freq_lon", "lat"])
    assert dims == set(ds_psd.dims.keys())
    
    ds_psd = psd_spacetime(ds, "ssh", ["lat", ])
    dims = set(["freq_lat", "lon", "time"])
    assert dims == set(ds_psd.dims.keys())
    
    # 2D CASES
    ds_psd = psd_spacetime(ds, "ssh", ["time", "lat"])
    dims = set(["freq_time", "freq_lat", "lon"])
    assert dims == set(ds_psd.dims.keys())
    
    ds_psd = psd_spacetime(ds, "ssh", ["time", "lon"])
    dims = set(["freq_time", "freq_lon", "lat"])
    assert dims == set(ds_psd.dims.keys())
    
    ds_psd = psd_spacetime(ds, "ssh", ["lat", "lon"])
    dims = set(["freq_lat", "freq_lon", "time"])
    assert dims == set(ds_psd.dims.keys())
    
def test_psd_isotropic_error():
    
    ds_ref = get_ssh_data()
    ds_model = ds_ref.copy()
    ds_model = ds_model.assign(study=ds_model["ssh"] + 0.01 * RNG.randn(*ds_model["ssh"].values.shape) * units.meter)
    
    # CASE I - non-average dimensions
    ds_psd = psd_isotropic_error(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=None
    )
    dims = set(["freq_r", "time"])
    assert dims == set(ds_psd.dims.keys())
    
    # CASE II - average dimensions
    ds_psd = psd_isotropic_error(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=["time"]
    )
    dims = set(["freq_r"])
    assert dims == set(ds_psd.dims.keys())
    
    
def test_psd_spacetime_error():
    
    ds_ref = get_ssh_data()
    ds_model = ds_ref.copy()
    ds_model = ds_model.assign(study=ds_model["ssh"] + 0.01 * RNG.randn(*ds_model["ssh"].values.shape) * units.meter)
    
    # CASE I - non-average dimensions
    ds_psd = psd_spacetime_error(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=None
    )
    dims = set(["freq_lat", "freq_lon", "time"])
    assert dims == set(ds_psd.dims.keys())
    
    # CASE II - average dimensions
    ds_psd = psd_spacetime_error(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=["time"]
    )
    dims = set(["freq_lat", "freq_lon",])
    assert dims == set(ds_psd.dims.keys())
    
    
def test_psd_isotropic_score():
    
    ds_ref = get_ssh_data()
    ds_model = ds_ref.copy()
    ds_model = ds_model.assign(study=ds_model["ssh"] + 0.01 * RNG.randn(*ds_model["ssh"].values.shape) * units.meter)
    ds_model = ds_model.pint.dequantify()
    
    # CASE I - non-average dimensions
    ds_psd, rs = psd_isotropic_score(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=None
    )
    dims = set(["freq_r", "time"])
    assert rs is None
    assert dims == set(ds_psd.dims.keys())
    assert ds_psd.min() >= 0.0
    assert ds_psd.max() <= 1.0
    assert ds_psd.mean() >= 0.99
    
    # CASE II - average dimensions
    ds_psd, rs = psd_isotropic_score(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=["time"]
    )
    dims = set(["freq_r"])
    assert rs is not  None
    assert dims == set(ds_psd.dims.keys())
    assert ds_psd.min() >= 0.0
    assert ds_psd.max() <= 1.0
    assert ds_psd.mean() >= 0.99
    
    
def test_psd_spacetime_score():
    
    ds_ref = get_ssh_data()
    ds_model = ds_ref.copy()
    ds_model = ds_model.assign(study=ds_model["ssh"] + 0.01 * RNG.randn(*ds_model["ssh"].values.shape) * units.meter)
    
    # CASE I - non-average dimensions
    ds_psd = psd_spacetime_score(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=None
    )[0]
    dims = set(["freq_lat", "freq_lon", "time"])
    assert dims == set(ds_psd.dims.keys())
    assert ds_psd.min() >= 0.0
    assert ds_psd.max() <= 1.0
    assert ds_psd.mean() >= 0.99
    
    # CASE II - average dimensions
    ds_psd = psd_spacetime_score(
        ds=ds_model, ref_variable="ssh", study_variable="study", 
        psd_dims=["lat", "lon"],
        avg_dims=["time"]
    )[0]
    dims = set(["freq_lat", "freq_lon"])
    assert dims == set(ds_psd.dims.keys())
    assert ds_psd.min() >= 0.0
    assert ds_psd.max() <= 1.0
    assert ds_psd.mean() >= 0.99

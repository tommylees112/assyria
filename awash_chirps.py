import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os
import netCDF4 as nc
import datetime as dt

# For parallel Computation
import dask
import xarray as xr
from dask import delayed
import dask.array as da

# LOAD DATA
data_dir = "africa_chirps_final.nc"
# dataset = nc.Dataset(data_dir,'r')
dataset = xr.open_dataset(data_dir, chunks={'latitude':10, 'longitude':10})

ds_by_month = dataset.groupby('time.month').mean('time')
stacked = ds_by_month.stack(allpoints=['latitude','longitude'])
global_mon_mean = stacked.groupby('allpoints').mean()

global_mon_mean.plot()
# stacked.groupby('allpoints').mean().to_netcdf('monmean.nc')
# ds = xr.open_dataset('monmean.nc')
# ds.plot()

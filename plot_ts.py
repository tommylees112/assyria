import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import netCDF4 as nc
import shapefile
from matplotlib import path
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import xarray as xr
import xarray.ufuncs as xu

# read in relevant data
data_dir = "/Users/TommyLees/Desktop/chirps_data/awash_analysis/africa_chirps_final_awash.nc"
chirps = nc.Dataset(data_dir,'r')
precip = np.array(chirps.variables['precip'])
lat = np.array(chirps.variables['latitude'])
lon = np.array(chirps.variables['longitude'])
time = np.array(chirps.variables['time'])
dataset = xr.open_dataset(data_dir, chunks={'time':108,'latitude':100, 'longitude':110})
datetime_ = numpy.array(dataset.time)

# read in shapefile
shp_dir = '/Users/TommyLees/Desktop/chirps_data/awash_analysis/awash_shp/Export_Output.shp'
sf = shapefile.Reader(shp_dir)
bbox = sf.bbox

# create a matplotlib Path object for cutting out a .shp
shape = sf.shapes()[0]
poly_points = shape.points
poly_path = path.Path(poly_points)

latmin = bbox[0]
lonmin = bbox[1]
latmax = bbox[2]
lonmax = bbox[3]

# create points (EQUIVALENT METHODS)
xx, yy = np.meshgrid(lon, lat)
xx, yy = xx.flatten(), yy.flatten()
points = np.array((xx, yy)).T
points2 = np.vstack((xx, yy)).T

flags = poly_path.contains_points(points)
flags2 = poly_path.contains_points(points2)

# MASK THE PRECIP ARRAY
shape_mask = flags.reshape(200,220)
# NOTE: need to invert this in order to use as a mask
# repeat the mask for all time steps
time_len = precip.shape[0]
shapemask_t = np.array([~shape_mask]*time_len)
# exclude negative (MISSING) values (e.g. -9999)
precip_mask = np.ma.array(precip, mask=np.logical_or(shapemask_t, precip < 0))

month_mean_raw = np.empty([12,200,220])
precip_anomaly_raw = np.empty([432,200,220])

# CALCULATE THE MONTH MEAN
for mth in range(12):
    monthly_precip = precip[mth::12,:,:] # get every yearly ts for that month (Jan 1980, Jan 1981, ...)
    mth_mean = monthly_precip.mean(axis=0)
    month_mean_raw[mth] = mth_mean

# CALCULATE THE ANOMALY FROM MONMEAN AT EACH TIMESTEP
for ts in range(timesteps):
    ts_anomaly = precip[ts, :, :] - month_mean_raw[ts % 12, :, :]
    precip_anomaly_raw[ts] = ts_anomaly

print(month_mean_raw.shape)
print(precip_anomaly_raw.shape)

# NOW MASK the array
precip_anomaly = np.ma.masked_array(precip_anomaly_raw, mask=np.logical_or(shapemask_t, precip < 0))

###############################################################################
# CHANGE THIS HERE

timseteps_to_plot = precip_anomaly.shape[0]
timseteps_to_plot = 2
###############################################################################

for ts in range(timseteps_to_plot):
    fig, ax = plt.subplots()

    data = precip_anomaly[ts, :, :]
    im = ax.pcolormesh(data, cmap='seismic_r', vmin=vmin, vmax=vmax)
    ts = pd.to_datetime(str(datetime_[mth]))
    d = ts.strftime('%Y-%m-%d')
    ax.set_title(f"{d} Precip Anomaly\n" + "($ precip_{t} - mean(precip_{month}) $)")
    # hide the axes labels (meaningless dims)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # zoom in to the correct area
    ax.set_ylim(55, 148)
    ax.set_xlim(58, 168)
    fig.colorbar(im)
    fig.savefig(f'/Users/TommyLees/Desktop/chirps_data/awash_analysis/figures/plots/{d}')
    plt.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import matplotlib.pyplot as plt
import numpy as np
import pdb
from mpl_toolkits.basemap import Basemap
from matplotlib import rc
rc('mathtext',default = 'regular')
import netCDF4 
from pycmbs.region import RegionBboxLatLon
from pycmbs.plots import GlobalMeanPlot
from pycmbs.examples import download
from pycmbs.data import Data
from pycmbs.mapping import map_plot
from pycmbs.diagnostic import PatternCorrelation
from pycmbs.region import RegionShape




def main():
    
    
    
    plt.close('all')
    
    shp_file = '/Users/mpim/Desktop/ben/TP/TibeatanPlateau'  # specify name of shapefile; note that it should be done WITHOUT the file extension
    
    
    # set a array as masked array: x.data = np.ma.array(arr, mask=arr!=arr)
    #set the region for masking
    r = RegionBboxLatLon(777, 70.,105.,25.,40., label='testregion')      
    r.mask = None
    
    
    #Read files 
    filename_Landevl ='/Users/mpim/Desktop/ben/chen_sebs_wgs84_n_0.13x0.13.nc'       #'/data/share/mpiles/TRS/m300157/land_eval/LandFluxEVAL.merged.89-05.monthly.diagnostic.nc'
    Landevl = Data(filename_Landevl, 'ETmon',read=True)     #'lat','lon', ET_mean
    
    #get aoi 
    Landevl.get_aoi_lat_lon(r)
    Landevl.cut_bounding_box()

    # read regions from shapefile
    # This gives an object which contains all regions stored in the shapefile
    
    RS = RegionShape(shp_file)
    
    # just print the region keys for illustration
    for k in RS.regions.keys():
        print k
    
    # if you now want to generate a particular mask we can do that
    # in the following example we mask the airt temperature for the
    # Tibetean plateau
    
    
    # and then mask it
    r_tibet = RS.regions[1]  # gives a Region object

    
    # mask with region

    Landevl.mask_region(r_tibet)
    Landevl.save('/Users/mpim/Desktop/ben/chen_sebs_recut2.nc') 

    
    
    plt.show()
    
    
    

    
if __name__ == "__main__":
    main()
 
 
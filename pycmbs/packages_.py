import datetime
import matplotlib.pyplot as plt
import numpy as np
import pdb
from mpl_toolkits.basemap import Basemap
from matplotlib import rc
rc('mathtext',default = 'regular')
import netCDF4
# from pycmbs.region import RegionBboxLatLon
from pycmbs.plots import GlobalMeanPlot
from pycmbs.examples import download
from pycmbs.data import Data
from pycmbs.mapping import map_plot
from pycmbs.diagnostic import PatternCorrelation
# from pycmbs.region import RegionShape

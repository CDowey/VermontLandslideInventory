# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 08:58:21 2019

@author: Colin.Dowey
"""

### Perform spatial analysis on all Landslides Inventoried in Vermont
### Extract elevation data from LiDAR for each landslide point
### Calculate distance from nearest river for each landslide point
### PLot histograms of landslides by elevation, distance from river and elevation vs. distance from river

# import requests
import geopandas as gpd
# import numpy as np
import matplotlib.pyplot as plt
# import rasterio as rio
from scipy import stats
from pathlib import Path

# Set working directory and file paths
wd = 
landslides_path = wd / 
NHD_path = wd / 
VTSP_NAD83_m_proj4 = '+proj=tmerc +lat_0=42.5 +lon_0=-72.5 +k=0.999964286 +x_0=500000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
landslides_output = wd / 

## Extract elevation data from Bare-Earth LiDAR DEM for each landslide inventory point

## Read in landslide spatial data. 
## We wil access the most up to date information from the open data portal
## From open data portal page we can find a link to a geojson of the landslide data under the API dropdown
#
#geojson_path = 'https://opendata.arcgis.com/datasets/3bd6e48efd30496d91d2f25817f3c40b_186.geojson'
#
#r = requests.get(geojson_path)
#data = r.json()
#
#landslides = gpd.GeoDataFrame.from_features(data['features'])


# The landslide shapefile already contains the elevation of the point performed in ArcGIS Pro
# At the moment I could not figure out how to best load the Statewide Lidar DEM into Python in a reasonable way
# Compiling the data into numpy array seems like the most reasonable approach I found so far but not implemented here.

landslides = gpd.read_file(str(landslides_path))
landslides = landslides.to_crs(VTSP_NAD83_m_proj4)

## Calculate the distance from each landslide point to the nearest stream or river

# Due to government shutdown link to USGS was not working. 
# So a local link is used. Could take the National Hydrology Dataset and clip to a buffered Vermont
NHD_flowline = gpd.read_file(str(NHD_path))
NHD_flowline = NHD_flowline.to_crs(VTSP_NAD83_m_proj4)

# Use geopandas point.distance to calculate the distance from each landslide point to the flowlines
# We only want to keep the minmum distance and add this to the landslides geodataframe
# point.distance works more simply with GeoDataSeries so I create a GeoDataSeries each for the landslide points and flowlines

min_dist = []

# As list comprehension
min_dist = [(min([point.distance(flowline) for flowline in NHD_flowline['geometry']])) for point in landslides['geometry']]

# As a for loop
#for point in landslides['geometry']:
#    min_dist.append(min([point.distance(flowline) for flowline in NHD_flowline['geometry']]))
    
landslides['min_dist_to_flowlines'] = min_dist

## Write the results of the nearest flowline analysis to shapefile
landslides.to_file(str(landslides_output))


## Matplotlib to create some basic plots

## Landslide Elevation
plt.figure()
# Set up histogram bins
bin_width = 10

# Start at elevation 0 is more clear than min elevation
min_bin = 0

# Sets the max of the bin range to be the next highest value divisible by 10 (the -1 part) than max value
max_bin = round(int(max(landslides['Elev_m']) + (bin_width/2)), -1)

bin_range = range(min_bin, max_bin + bin_width, bin_width)

plt.hist(landslides['Elev_m'], bin_range)

# Set plot x limts
axes = plt.gca()
axes.set_xlim(min_bin, max_bin)

# Set axis lables
axes.set_xlabel('Landslide Elevation (m)')
axes.set_ylabel('Count')
axes.set_title('Vermont Landslide Elevation Distribution')

## Landslide Distance from Rivers
plt.figure()
# Set up histogram bins
bin_width = 10

# Start at elevation 0 is more clear than min elevation
min_bin = 0

# Sets the max of the bin range to be the next highest value divisible by 10 (the -1 part) than max value
max_bin = round(int(max(landslides['min_dist_to_flowlines']) + (bin_width/2)), -1)

bin_range = range(min_bin, max_bin + bin_width, bin_width)

plt.hist(landslides['min_dist_to_flowlines'], bin_range)

# Set plot x limts
axes = plt.gca()
axes.set_xlim(min_bin, max_bin)

# Set axis lables
axes.set_xlabel('Distance to nearest flowline (m)')
axes.set_ylabel('Count')
axes.set_title('Vermont Landslide Distance from Flowlines')


## Landslide Elevation vs. Distance from rivers
plt.figure()
# Linear regression elev vs Dist
slope, intercept, r_value, p_value, std_err = stats.linregress(landslides['min_dist_to_flowlines'], landslides['Elev_m'])
line = slope * landslides['min_dist_to_flowlines'] + intercept

# Plot with linear regression line
plt.plot(landslides['min_dist_to_flowlines'], landslides['Elev_m'], '.', landslides['min_dist_to_flowlines'], line, 'b-')

# Plot just scatter plot
#plt.scatter(landslides['min_dist_to_flowlines'], landslides['Elev_m'], s = 5)

# Set plot x limts
axes = plt.gca()
axes.set_xlim(0, max(landslides['min_dist_to_flowlines']) + 20)
axes.set_ylim(0, max(landslides['Elev_m']) + 20)

# Set axis lables
axes.set_xlabel('Distance to nearest flowline (m)')
axes.set_ylabel('Elevation (m)')
axes.set_title('Vermont Landslide Distance from Flowlines vs. Elevation')











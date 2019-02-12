# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 09:03:33 2019

@author: Colin.Dowey
"""

# This script extracts information from rasters for each point in the Vermont Geological Survey's Landslide Inventory

import requests
import geopandas as gpd

# Read in the most up to date Landslide Inventory from the geodata.vermont.gov to a GeoDataFrame
landslides_geojson = 'https://opendata.arcgis.com/datasets/3bd6e48efd30496d91d2f25817f3c40b_186.geojson'

# Read geojson into GeoDataFrame
r = requests.get(landslides_geojson)
data = r.json()
landslides = gpd.GeoDataFrame.from_features(data)
landslides.crs = {'init': 'epsg:4326'}

landslides = landslides.to_crs({'init': 'epsg:32145'})

# Extract Elevation information from LiDAR DEM hosted on VCGI Image Server

DEM_ImageServer_url = 'https://maps.vcgi.vermont.gov/arcgis/rest/services/EGC_services/IMG_VCGI_LIDARDEM_SP_NOCACHE_v1/ImageServer/'

DEM_elev = []

for index, slide in enumerate(landslides['geometry']):

    x = str(slide.x)
    y = str(slide.y)

    print('Elev: ' + str(index))
    
    req_url = DEM_ImageServer_url + 'identify?geometry=' + x + '%2C+' + y + '&geometryType=esriGeometryPoint&mosaicRule=&renderingRule=&renderingRules=&pixelSize=&time=&returnGeometry=false&returnCatalogItems=false&f=pjson'

    req = requests.get(req_url)
    rast_dict = req.json()
    rast_val = rast_dict['value']
    
    DEM_elev.append(rast_val)
   
landslides.loc[:,'LiDAR_Elev_m'] = None
landslides.loc[:,'LiDAR_Elev_m'] = DEM_elev

# Extract Slope information from LiDAR Slope hosted on VCGI Image Server

Slope_ImageServer_url = 'https://maps.vcgi.vermont.gov/arcgis/rest/services/EGC_services/IMG_VCGI_LIDARSLOPE_SP_NOCACHE_v1/ImageServer/'

Slope = []

for index, slide in enumerate(landslides['geometry']):

    x = str(slide.x)
    y = str(slide.y)

    print('Slope: ' + str(index))
    
    req_url = Slope_ImageServer_url + 'identify?geometry=' + x + '%2C+' + y + '&geometryType=esriGeometryPoint&mosaicRule=&renderingRule=&renderingRules=&pixelSize=&time=&returnGeometry=false&returnCatalogItems=false&f=pjson'

    req = requests.get(req_url)
    rast_dict = req.json()
    rast_val = rast_dict['value']
    
    Slope.append(rast_val)
   
landslides.loc[:,'LiDAR_Slope'] = None
landslides.loc[:,'LiDAR_Slope'] = Slope

# Extract Aspect information from LiDAR Slope hosted on VCGI Image Server

Aspect_ImageServer_url = 'https://maps.vcgi.vermont.gov/arcgis/rest/services/EGC_services/IMG_VCGI_LIDARASPECT_SP_NOCACHE_v1/ImageServer/'

Aspect = []

for index, slide in enumerate(landslides['geometry']):

    x = str(slide.x)
    y = str(slide.y)

    print('Aspect: ' + str(index))
    
    req_url = Aspect_ImageServer_url + 'identify?geometry=' + x + '%2C+' + y + '&geometryType=esriGeometryPoint&mosaicRule=&renderingRule=&renderingRules=&pixelSize=&time=&returnGeometry=false&returnCatalogItems=false&f=pjson'

    req = requests.get(req_url)
    rast_dict = req.json()
    rast_val = rast_dict['value']
    
    Aspect.append(rast_val)
   
landslides.loc[:,'LiDAR_Aspect'] = None
landslides.loc[:,'LiDAR_Aspect'] = Aspect
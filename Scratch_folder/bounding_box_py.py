# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 11:35:49 2025

@author: tjmayer
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import box

# Load CSV
df = pd.read_csv('converted_coordinates.csv')

# Replace these with the actual column names if different
lat_col = 'Latitude'
lon_col = 'Longitude'

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
    crs='EPSG:4326'
)

# Get the total bounds: (minx, miny, maxx, maxy)
minx, miny, maxx, maxy = gdf.total_bounds

# Create a bounding box polygon
bounding_box = box(minx, miny, maxx, maxy)

# Create a GeoDataFrame for the bounding box
bbox_gdf = gpd.GeoDataFrame(
    index=[0],
    geometry=[bounding_box],
    crs='EPSG:4326'
)

# Save as GeoJSON
bbox_gdf.to_file('bounding_box.geojson', driver='GeoJSON')
print("finished")
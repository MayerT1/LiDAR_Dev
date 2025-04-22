# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 16:07:52 2025

@author: tjmayer
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Distance threshold in meters
DISTANCE_THRESHOLD = 25


#rh98

# Load GEDI data  #GEDI_L2A_spatial_rh98_data.csv'
# gedi_df = pd.read_csv('GEDI_L2A_spatial_rh98_data.csv')   
# gedi_gdf = gpd.GeoDataFrame(
#     gedi_df,
#     geometry=gpd.points_from_xy(gedi_df.Longitude, gedi_df.Latitude),
#     crs="EPSG:4326"  # WGS84
# ).to_crs(epsg=3857)  # Project to meters
# print("load data 1")

gedi_df = pd.read_csv('GEDI_L2A_L2B_spatial_filtered.csv')   
gedi_gdf = gpd.GeoDataFrame(
    gedi_df,
    geometry=gpd.points_from_xy(gedi_df.Longitude, gedi_df.Latitude),
    crs="EPSG:4326"  # WGS84
).to_crs(epsg=3857)  # Project to meters
print("load data 1")

print(gedi_gdf)
# Get the head of the DataFrame as a list
df_head_list = gedi_gdf.head().values.tolist()

# Print the list
# print("df_head_list",df_head_list)

#Lidar_z

# Load converted ALS data
als_df = pd.read_csv('converted_coordinates.csv')
als_gdf = gpd.GeoDataFrame(
    als_df,
    geometry=gpd.points_from_xy(als_df.Longitude, als_df.Latitude),
    crs="EPSG:4326"
).to_crs(epsg=3857)
print("load data 2")
print(als_gdf)

# Spatial join based on distance
joined = gpd.sjoin_nearest(
    gedi_gdf, als_gdf, how="inner", max_distance=DISTANCE_THRESHOLD, distance_col="distance"
)


# # Keep only relevant columns and save
# joined[['beam', 'shot_number', 'latitude_left', 'longitude_left', 'rh98_GEDI2A', 'Lidar_z', 'distance']].rename(columns={
#     'latitude_left': 'Latitude',
#     'longitude_left': 'Longitude'
# }).to_csv('gediA_B_als_spatially_joined_within_25m.csv', index=False)


# Keep only relevant columns and save
joined[['beam', 'shot_number', 'rh98_GEDI2A', 'Lidar_z', 'distance']].to_csv('zzgediA_B_als_spatially_joined_within_25m.csv', index=False)
print(joined)


print("Spatial join completed. Saved to 'zzgedi_als_spatially_joined_within_25m.csv'")

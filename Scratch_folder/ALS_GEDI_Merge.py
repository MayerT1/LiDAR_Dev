# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 09:24:41 2025

@author: tjmayer
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 1. Load GEDI data and drop rows where rh98_GEDI2A is 0
gedi_df = pd.read_csv('GEDI_L2A_L2B_spatial_filtered.csv')
gedi_df_filtered = gedi_df[gedi_df['rh98_GEDI2A'] != 0]

print("gedi_df_filtered", gedi_df_filtered)

# Create geometry for GEDI points
gedi_gdf = gpd.GeoDataFrame(
    gedi_df_filtered,
    geometry=gpd.points_from_xy(gedi_df_filtered['Longitude'], gedi_df_filtered['Latitude']),
    crs="EPSG:4326"
)

# 2. Load converted coordinates data and create geometry
converted_df = pd.read_csv('converted_coordinates.csv')
converted_gdf = gpd.GeoDataFrame(
    converted_df,
    geometry=gpd.points_from_xy(converted_df['Longitude'], converted_df['Latitude']),
    crs="EPSG:4326"
)

# Convert to a metric projection for accurate distance calculation
gedi_gdf = gedi_gdf.to_crs(epsg=3857)
converted_gdf = converted_gdf.to_crs(epsg=3857)

# 3. Perform spatial join using a 25 meter buffer
converted_buffered = converted_gdf.copy()
converted_buffered['geometry'] = converted_buffered.geometry.buffer(25)

# Perform spatial join (left: GEDI, right: buffered converted)
joined_gdf = gpd.sjoin(gedi_gdf, converted_buffered, how='inner', predicate='intersects')
print("joined_gdf", joined_gdf)


# Select required columns
final_fields_gedi = [
    'file', 'beam', 'shot_number', 'Latitude_left', 'Longitude_left',
    'rh98_GEDI2A', 'rh100_GEDI2A', 'elev_highest_GEDI2A', 'elev_lowest_GEDI2A',
    'height_lastbin_GEDI2A', 'sensitivity_GEDI2A', 'l2a_quality_flag_GEDI2A',
    'cover_GEDI2B', 'pai_GEDI2B', 'fhd_normal_GEDI2B', 'omega_GEDI2B',
    'pgap_theta_GEDI2B', 'pgap_theta_error_GEDI2B', 'lat_GEDI2B', 'lon_GEDI2B',
    'l2b_quality_flag_GEDI2B'
]
final_fields_converted = ['Lidar_z', 'Intensity', 'Latitude_right', 'Longitude_right']

# Rename Latitude/Longitude columns to avoid confusion
joined_gdf = joined_gdf.rename(columns={
    'Latitude_left': 'Latitude', 'Longitude_left': 'Longitude',
    'Latitude_right': 'Lidar_Latitude', 'Longitude_right': 'Lidar_Longitude'
})

final_columns = [
    'file', 'beam', 'shot_number', 'Latitude', 'Longitude',
    'rh98_GEDI2A', 'rh100_GEDI2A', 'elev_highest_GEDI2A', 'elev_lowest_GEDI2A',
    'height_lastbin_GEDI2A', 'sensitivity_GEDI2A', 'l2a_quality_flag_GEDI2A',
    'cover_GEDI2B', 'pai_GEDI2B', 'fhd_normal_GEDI2B', 'omega_GEDI2B',
    'pgap_theta_GEDI2B', 'pgap_theta_error_GEDI2B', 'lat_GEDI2B', 'lon_GEDI2B',
    'l2b_quality_flag_GEDI2B', 'Lidar_z', 'Intensity', 'Lidar_Latitude', 'Lidar_Longitude'
]

# Save final merged data
joined_gdf[final_columns].to_csv('GEDI_spatially_merged.csv', index=False)
print("finished")

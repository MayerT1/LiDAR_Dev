import os
# import laspy
import pandas as pd
import geopandas as gpd
from scipy.stats import spearmanr
from shapely.geometry import Point


veg_df = pd.read_csv("veg.csv")  # change to your actual file name
print("upload 1")
lidar_df = pd.read_csv("converted_coordinates.csv")  # change to your actual file name
print("upload 2")

# Convert LiDAR and Veg data to GeoDataFrames for spatial joining
lidar_gdf = gpd.GeoDataFrame(lidar_df, geometry=gpd.points_from_xy(lidar_df["Longitude"], lidar_df["Latitude"]))
print("geo 1")
veg_gdf = gpd.GeoDataFrame(veg_df, geometry=gpd.points_from_xy(veg_df["adjDecimalLongitude"], veg_df["adjDecimalLatitude"]))
print("geo 2")

# Perform a spatial join to find overlapping LiDAR and vegetation data
merged_gdf = gpd.sjoin_nearest(veg_gdf, lidar_gdf, how="inner")  # Adjust distance threshold # max_distance=50000
print("merge")

# Compute correlation between LiDAR elevation and vegetation height
if "height" in merged_gdf.columns:  # Ensure 'height' exists in the Veg data
    correlation, p_value = spearmanr(merged_gdf["Lidar_z"], merged_gdf["height"])
    print(f"Spearman Correlation: {correlation}, p-value: {p_value}")
else:
    print("No 'height' column found in vegetation data. Check column names.")

# Save merged data for further analysis
merged_gdf.to_csv("lidar_veg_correlation.csv", index=False)
print("Merged dataset saved as 'lidar_veg_correlation.csv'.")

print("finish")
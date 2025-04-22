import pandas as pd
from pyproj import Transformer

print("start")

# Load your CSV (make sure the file is in the same directory or give full path)
df = pd.read_csv("lidar_gdf.csv")  # change to your actual file name

# Set up the transformer (update EPSG code if needed)
transformer = Transformer.from_crs("EPSG:32619", "EPSG:4326", always_xy=True)

# Function to convert a row
def convert_coords(row):
    lon, lat = transformer.transform(row['Easting'], row['Northing'])
    print("in the loop")
    return pd.Series({'Latitude': lat, 'Longitude': lon})
print("out loop")
# Apply conversion
df[['Latitude', 'Longitude']] = df.apply(convert_coords, axis=1)

# Save results to a new CSV
df.to_csv("converted_coordinates.csv", index=False)

print("Conversion complete! Saved to converted_coordinates.csv")
print("finish")
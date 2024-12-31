import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium


import geopandas as gpd
import pandas as pd


# Unzip the file
import zipfile
import os

zip_file = 'gadm41_MYS_shp.zip'
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall('gadm41_MYS_shp')

# Load the shapefile using GeoPandas
shapefile_path = 'gadm41_MYS_shp/gadm41_MYS_1.shp'  # Adjust path if necessary
gdf = gpd.read_file(shapefile_path)

# Preview the data
print("Shapefile loaded successfully. Here is the first few rows of the data:")
print(gdf.head())

# Extract relevant data (e.g., Name, Latitude, Longitude, and Description)
# Assuming the shapefile contains relevant information in columns
print("\nColumns in the shapefile:")
print(gdf.columns)

# If you need to compute centroids for mapping
gdf['Latitude'] = gdf.geometry.centroid.y
gdf['Longitude'] = gdf.geometry.centroid.x

# Select relevant columns for tourist attractions
# Adjust column names as per your data
df_cleaned = gdf[['NAME_1', 'Latitude', 'Longitude']].copy()
df_cleaned.rename(columns={'NAME_1': 'Name'}, inplace=True)

# Add a placeholder for descriptions (if not available)
df_cleaned['Description'] = "Tourist attraction in Malaysia."

# Save the cleaned data
output_file = 'cleaned_tourist_attractions_from_shapefile.csv'
df_cleaned.to_csv(output_file, index=False)

print(f"\nData cleaned and saved to {output_file}.")

# File upload feature
st.title("Map of Tourist Attractions in Malaysia")
uploaded_file = st.file_uploader("Upload a CSV file containing tourist attractions", type=["csv"])

if uploaded_file:
    # Read the CSV file uploaded by the user
    df = pd.read_csv(uploaded_file)

    # Verify if the required columns are present
    required_columns = {'Name', 'Description', 'Latitude', 'Longitude'}
    if not required_columns.issubset(df.columns):
        st.error(f"The CSV file is missing the required columns: {required_columns - set(df.columns)}")
    else:
        # Automatically classify attraction types (if not provided)
        if 'Type' not in df.columns:
            df['Type'] = [
                'Natural' if i % 3 == 0 else 'Cultural' if i % 3 == 1 else 'Historical'
                for i in range(len(df))
            ]
# Load your dataset (replace with the path to your actual CSV file)
data_file = 'cleaned_tourist_attractions_from_shapefile.csv'  # Path to your CSV file
df = pd.read_csv(data_file)

# Check the dataset to ensure it has the necessary columns: Name, Description, Latitude, Longitude
print(df.head())
        # Set map center to Malaysia
        map_center = [4.2105, 101.9758]  # Coordinates for the center of Malaysia
        tourist_map = folium.Map(location=map_center, zoom_start=6)

        # Create groups for different types of attractions
        natural_group = folium.FeatureGroup(name='Natural Attractions')
        cultural_group = folium.FeatureGroup(name='Cultural Attractions')
        historical_group = folium.FeatureGroup(name='Historical Attractions')

        # Add markers
        for _, row in df.iterrows():
            name = row['Name']
            description = row['Description']
            latitude = row['Latitude']
            longitude = row['Longitude']
            type_ = row['Type']

            # Set marker color and icon based on type
            if type_ == 'Historical':
                color = 'red'
                icon = 'info-sign'
                group = historical_group
            elif type_ == 'Natural':
                color = 'green'
                icon = 'leaf'
                group = natural_group
            elif type_ == 'Cultural':
                color = 'purple'
                icon = 'education'
                group = cultural_group
            else:
                color = 'gray'
                icon = 'question'
                group = natural_group  # Default category

            # Add marker
            popup_text = f"<b>{name}</b><br>{description}"
            folium.Marker(
                location=[latitude, longitude],
                popup=folium.Popup(popup_text, max_width=250),
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(group)

        # Add groups to the map
        natural_group.add_to(tourist_map)
        cultural_group.add_to(tourist_map)
        historical_group.add_to(tourist_map)

        # Add layer control
        folium.LayerControl().add_to(tourist_map)

        # Display total number of attractions
        total_attractions = len(df)
        total_popup_text = f"Total number of attractions: {total_attractions}"
        folium.Marker(
            location=map_center,
            popup=folium.Popup(total_popup_text, max_width=250),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(tourist_map)

        # Display the map in Streamlit
        st_folium(tourist_map, width=700, height=500)

        # Display total number of attractions in the sidebar
        st.sidebar.header("Overview of Tourist Attractions")
        st.sidebar.write(f"Total number of attractions: {total_attractions}")

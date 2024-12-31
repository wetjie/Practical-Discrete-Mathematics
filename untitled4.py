import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# Title
st.title("Map of Tourist Attractions in Malaysia")

# Specify the path to the CSV file
csv_file_path = "cleaned_tourist_attractions_from_shapefile (1).csv"  # Replace with the actual path to your CSV file

try:
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

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

        # Display the first few rows of the data
        st.write("Loaded data:")
        st.write(df.head())

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
except FileNotFoundError:
    st.error(f"The file {csv_file_path} was not found. Please ensure the file exists at the specified path.")

import streamlit as st
import geopandas as gpd
import pandas as pd
import zipfile
import os

# 设置标题
st.title("马来西亚旅游景点数据处理")

# 上传 ZIP 文件
uploaded_file = st.file_uploader("上传包含马来西亚地图的 ZIP 文件", type=["zip"])

if uploaded_file:
    # 保存上传的文件
    zip_file_path = "uploaded_file.zip"
    with open(zip_file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    # 解压 ZIP 文件
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("shapefile_data")
    
    st.success("ZIP 文件解压成功！")

    # 查找 Shapefile 路径
    shapefile_dir = "shapefile_data"
    shapefile_path = None
    for root, dirs, files in os.walk(shapefile_dir):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                break
        if shapefile_path:
            break

    if shapefile_path:
        st.write(f"找到 Shapefile 文件: {shapefile_path}")
        
        # 加载 Shapefile 数据
        try:
            gdf = gpd.read_file(shapefile_path)
            st.success("Shapefile 加载成功！")
            
            # 显示数据预览
            st.write("数据预览:")
            st.write(gdf.head())
            
            # 添加经纬度信息
            gdf['Latitude'] = gdf.geometry.centroid.y
            gdf['Longitude'] = gdf.geometry.centroid.x
            
            # 选择相关列
            df_cleaned = gdf[['NAME_1', 'Latitude', 'Longitude']].copy()
            df_cleaned.rename(columns={'NAME_1': 'Name'}, inplace=True)
            df_cleaned['Description'] = "Tourist attraction in Malaysia."
            
            # 显示清理后的数据
            st.write("清理后的数据:")
            st.write(df_cleaned)
            
            # 保存清理后的数据
            output_file = "cleaned_tourist_attractions_from_shapefile.csv"
            df_cleaned.to_csv(output_file, index=False)
            st.success(f"清理后的数据已保存到 {output_file}")
            
            # 提供下载链接
            with open(output_file, "rb") as f:
                st.download_button(
                    label="下载清理后的数据",
                    data=f,
                    file_name="cleaned_tourist_attractions_from_shapefile.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"加载 Shapefile 失败: {e}")
    else:
        st.error("未找到有效的 Shapefile 文件，请确保 ZIP 文件中包含 .shp 文件。")








"""b. Map visualisations                                                                                

• Use any relevant and suitable python library to create an interactive map.

• Plot the locations of the tourist attractions on map with markers.

• Each marker should display the name and description of the attraction when
clicked.
"""

import folium
import pandas as pd

# Load your dataset (replace with the path to your actual CSV file)
data_file = 'cleaned_tourist_attractions_from_shapefile.csv'  # Path to your CSV file
df = pd.read_csv(data_file)

# Check the dataset to ensure it has the necessary columns: Name, Description, Latitude, Longitude
print(df.head())

# Create a base map centered around Malaysia
map_center = [4.2105, 101.9758]  # Latitude, Longitude of Malaysia's center
tourist_map = folium.Map(location=map_center, zoom_start=6)

# Loop through the dataframe to add markers for each attraction
for _, row in df.iterrows():
    attraction_name = row['Name']
    attraction_description = row['Description']
    latitude = row['Latitude']
    longitude = row['Longitude']

    # Create popup text for each marker
    popup_text = f"<b>{attraction_name}</b><br>{attraction_description}"

    # Create a marker for each attraction
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(tourist_map)

# Display the map directly in Google Colab
tourist_map

"""c.Customisations                                                                                        

• Customise the map by adding different marker colours based on the type
of attraction (Eg: historical site, natural wonder, amusement park)

• Add a layer control to toggle different types of attractions on and off.
"""

import folium
import pandas as pd

# Load your dataset (replace with the path to your actual CSV file)
data_file = 'cleaned_tourist_attractions_from_shapefile.csv'  # Path to your dataset
df = pd.read_csv(data_file)

# Manually add the 'Type' column for each attraction
df['Type'] = [
    'Natural',       # Johor
    'Cultural',      # Kedah
    'Natural',       # Kelantan
    'Historical',    # Kuala Lumpur
    'Cultural',      # Labuan
    'Cultural',      # Penang
    'Natural',       # Perak
    'Natural',       # Perlis
    'Natural',       # Pahang
    'Natural',       # Sabah
    'Natural',       # Sarawak
    'Cultural',      # Selangor
    'Historical',    # Melaka
    'Cultural',      # Negeri Sembilan
    'Natural',       # Terengganu
    'Cultural'       # Putrajaya
]

# Check the updated dataframe
print(df.head())

# Create the map centered around Malaysia
map_center = [4.2105, 101.9758]  # Latitude, Longitude of Malaysia's center
tourist_map = folium.Map(location=map_center, zoom_start=6)

# Create FeatureGroups for different types of attractions
natural_group = folium.FeatureGroup(name='Natural Attractions')
cultural_group = folium.FeatureGroup(name='Cultural Attractions')
historical_group = folium.FeatureGroup(name='Historical Attractions')

# Create markers for each type of attraction
for _, row in df.iterrows():
    attraction_name = row['Name']
    attraction_description = row['Description']
    latitude = row['Latitude']
    longitude = row['Longitude']
    attraction_type = row['Type']  # Get the type from the updated 'Type' column

    # Set different colors and icons for each type of attraction
    if attraction_type == 'Historical':
        marker_color = 'red'
        marker_icon = 'info-sign'
        group = historical_group
    elif attraction_type == 'Natural':
        marker_color = 'green'
        marker_icon = 'leaf'
        group = natural_group
    elif attraction_type == 'Cultural':
        marker_color = 'purple'
        marker_icon = 'education'
        group = cultural_group
    else:
        marker_color = 'gray'
        marker_icon = 'question'
        group = natural_group  # Default to the natural attractions group for uncategorized attractions

    # Create the popup text
    popup_text = f"<b>{attraction_name}</b><br>{attraction_description}"

    # Create the marker and add it to the corresponding group
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color=marker_color, icon=marker_icon)
    ).add_to(group)

# Add all the feature groups to the map
natural_group.add_to(tourist_map)
cultural_group.add_to(tourist_map)
historical_group.add_to(tourist_map)

# Add a layer control to allow toggling between different attraction types
folium.LayerControl().add_to(tourist_map)

# Display the map in Google Colab
tourist_map

"""d. Additional features                   

• Add a feature to display the total number of attractions on the map.

• Host the map on streamlit / Shiny for python / any relevant server/ cloud.
"""



import folium
import pandas as pd

# Load your dataset (replace with the path to your actual CSV file)
data_file = 'cleaned_tourist_attractions_from_shapefile.csv'  # Path to your dataset
df = pd.read_csv(data_file)

# Manually add the 'Type' column for each attraction (adjusted for your dataset)
df['Type'] = [
    'Natural',       # Johor
    'Cultural',      # Kedah
    'Natural',       # Kelantan
    'Historical',    # Kuala Lumpur
    'Cultural',      # Labuan
    'Cultural',      # Penang
    'Natural',       # Perak
    'Natural',       # Perlis
    'Natural',       # Pahang
    'Natural',       # Sabah
    'Natural',       # Sarawak
    'Cultural',      # Selangor
    'Historical',    # Melaka
    'Cultural',      # Negeri Sembilan
    'Natural',       # Terengganu
    'Cultural'       # Putrajaya
]

# Check the updated dataframe
print(df.head())

# Create the map centered around Malaysia
map_center = [4.2105, 101.9758]  # Latitude, Longitude of Malaysia's center
tourist_map = folium.Map(location=map_center, zoom_start=6)

# Create FeatureGroups for different types of attractions
natural_group = folium.FeatureGroup(name='Natural Attractions')
cultural_group = folium.FeatureGroup(name='Cultural Attractions')
historical_group = folium.FeatureGroup(name='Historical Attractions')

# Create markers for each type of attraction
for _, row in df.iterrows():
    attraction_name = row['Name']
    attraction_description = row['Description']
    latitude = row['Latitude']
    longitude = row['Longitude']
    attraction_type = row['Type']  # Get the type from the updated 'Type' column

    # Set different colors and icons for each type of attraction
    if attraction_type == 'Historical':
        marker_color = 'red'
        marker_icon = 'info-sign'
        group = historical_group
    elif attraction_type == 'Natural':
        marker_color = 'green'
        marker_icon = 'leaf'
        group = natural_group
    elif attraction_type == 'Cultural':
        marker_color = 'purple'
        marker_icon = 'education'
        group = cultural_group
    else:
        marker_color = 'gray'
        marker_icon = 'question'
        group = natural_group  # Default to the natural attractions group for uncategorized attractions

    # Create the popup text
    popup_text = f"<b>{attraction_name}</b><br>{attraction_description}"

    # Create the marker and add it to the corresponding group
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color=marker_color, icon=marker_icon)
    ).add_to(group)

# Add all the feature groups to the map
natural_group.add_to(tourist_map)
cultural_group.add_to(tourist_map)
historical_group.add_to(tourist_map)

# Add a layer control to allow toggling between different attraction types
folium.LayerControl().add_to(tourist_map)

# Add a feature to display the total number of attractions on the map
total_attractions = len(df)
total_popup_text = f"Total number of attractions: {total_attractions}"

# Add a marker to display the total number of attractions at the center of the map
folium.Marker(
    location=map_center,
    popup=folium.Popup(total_popup_text, max_width=250),
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(tourist_map)

# Display the map directly in Google Colab
tourist_map

import folium
import pandas as pd
import streamlit as st

# Load your dataset (replace with the path to your actual CSV file)
data_file = 'cleaned_tourist_attractions_from_shapefile.csv'  # Path to your dataset
df = pd.read_csv(data_file)

# Manually add the 'Type' column for each attraction
df['Type'] = [
    'Natural',       # Johor
    'Cultural',      # Kedah
    'Natural',       # Kelantan
    'Historical',    # Kuala Lumpur
    'Cultural',      # Labuan
    'Cultural',      # Penang
    'Natural',       # Perak
    'Natural',       # Perlis
    'Natural',       # Pahang
    'Natural',       # Sabah
    'Natural',       # Sarawak
    'Cultural',      # Selangor
    'Historical',    # Melaka
    'Cultural',      # Negeri Sembilan
    'Natural',       # Terengganu
    'Cultural'       # Putrajaya
]

# Create the map centered around Malaysia
map_center = [4.2105, 101.9758]  # Latitude, Longitude of Malaysia's center
tourist_map = folium.Map(location=map_center, zoom_start=6)

# Create FeatureGroups for different types of attractions
natural_group = folium.FeatureGroup(name='Natural Attractions')
cultural_group = folium.FeatureGroup(name='Cultural Attractions')
historical_group = folium.FeatureGroup(name='Historical Attractions')

# Create markers for each type of attraction
for _, row in df.iterrows():
    attraction_name = row['Name']
    attraction_description = row['Description']
    latitude = row['Latitude']
    longitude = row['Longitude']
    attraction_type = row['Type']  # Get the type from the updated 'Type' column

    # Set different colors and icons for each type of attraction
    if attraction_type == 'Historical':
        marker_color = 'red'
        marker_icon = 'info-sign'
        group = historical_group
    elif attraction_type == 'Natural':
        marker_color = 'green'
        marker_icon = 'leaf'
        group = natural_group
    elif attraction_type == 'Cultural':
        marker_color = 'purple'
        marker_icon = 'education'
        group = cultural_group
    else:
        marker_color = 'gray'
        marker_icon = 'question'
        group = natural_group  # Default to the natural attractions group for uncategorized attractions

    # Create the popup text
    popup_text = f"<b>{attraction_name}</b><br>{attraction_description}"

    # Create the marker and add it to the corresponding group
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color=marker_color, icon=marker_icon)
    ).add_to(group)

# Add all the feature groups to the map
natural_group.add_to(tourist_map)
cultural_group.add_to(tourist_map)
historical_group.add_to(tourist_map)

# Add a layer control to allow toggling between different attraction types
folium.LayerControl().add_to(tourist_map)

# Add a feature to display the total number of attractions on the map
total_attractions = len(df)
total_popup_text = f"Total number of attractions: {total_attractions}"

# Add a marker to display the total number of attractions at the center of the map
folium.Marker(
    location=map_center,
    popup=folium.Popup(total_popup_text, max_width=250),
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(tourist_map)

# Display the map in Streamlit
# To display the map in Streamlit, we need to use Streamlit-Folium integration
from streamlit_folium import st_folium

# Display the map in the Streamlit app
st.title("Tourist Attractions in Malaysia")
st_folium(tourist_map, width=700, height=500)

# Show the total number of attractions on the sidebar
st.sidebar.header("Tourist Attractions Overview")
st.sidebar.write(f"Total Number of Attractions: {total_attractions}")


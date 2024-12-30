import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# 上传文件功能
st.title("马来西亚旅游景点地图")
uploaded_file = st.file_uploader("上传包含旅游景点的 CSV 文件", type=["csv"])

if uploaded_file:
    # 读取用户上传的 CSV 文件
    df = pd.read_csv(uploaded_file)

    # 验证数据是否包含必要列
    required_columns = {'Name', 'Description', 'Latitude', 'Longitude'}
    if not required_columns.issubset(df.columns):
        st.error(f"CSV 文件缺少必要列：{required_columns - set(df.columns)}")
    else:
        # 自动分类景点类型（如果没有提供）
        if 'Type' not in df.columns:
            df['Type'] = [
                'Natural' if i % 3 == 0 else 'Cultural' if i % 3 == 1 else 'Historical'
                for i in range(len(df))
            ]

        # 显示上传的前几行数据
        st.write("已加载数据：")
        st.write(df.head())

        # 地图中心设置为马来西亚
        map_center = [4.2105, 101.9758]  # 马来西亚的中心坐标
        tourist_map = folium.Map(location=map_center, zoom_start=6)

        # 创建不同类型景点的分组
        natural_group = folium.FeatureGroup(name='自然景点')
        cultural_group = folium.FeatureGroup(name='文化景点')
        historical_group = folium.FeatureGroup(name='历史景点')

        # 添加标记
        for _, row in df.iterrows():
            name = row['Name']
            description = row['Description']
            latitude = row['Latitude']
            longitude = row['Longitude']
            type_ = row['Type']

            # 根据类型设置标记颜色和图标
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
                group = natural_group  # 默认分类

            # 添加标记
            popup_text = f"<b>{name}</b><br>{description}"
            folium.Marker(
                location=[latitude, longitude],
                popup=folium.Popup(popup_text, max_width=250),
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(group)

        # 添加分组到地图
        natural_group.add_to(tourist_map)
        cultural_group.add_to(tourist_map)
        historical_group.add_to(tourist_map)

        # 添加图层控制
        folium.LayerControl().add_to(tourist_map)

        # 显示景点总数
        total_attractions = len(df)
        total_popup_text = f"总景点数：{total_attractions}"
        folium.Marker(
            location=map_center,
            popup=folium.Popup(total_popup_text, max_width=250),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(tourist_map)

        # 在 Streamlit 中展示地图
        st_folium(tourist_map, width=700, height=500)

        # 在侧边栏显示总景点数
        st.sidebar.header("旅游景点概览")
        st.sidebar.write(f"总景点数：{total_attractions}")

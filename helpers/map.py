import folium
import pandas as pd
from streamlit_folium import st_folium
import pathlib
import json
import numpy as np
import random
import geopandas as gpd
from typing import Union, Sequence, Tuple, List


COUNTRIES = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'The Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
             'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada',
             'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Democratic Republic of the Congo', 'Republic of the Congo', 'Costa Rica', 'Côte d’Ivoire', 'Croatia', 'Cuba', 'Cyprus',
             'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor (Timor-Leste)', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia',
             'Fiji', 'Finland', 'France', 'Gabon', 'The Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India',
             'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea', 'South Korea', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
             'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico',
             'Micronesia, Federated States of', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger',
             'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda',
             'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore',
             'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Sudan, South', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand',
             'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'England', 'Wales', 'Scotland', 'Ireland', 'United States', 'Uruguay',
             'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']


def calculate_sw_ne_c_coordinates(geojson_data) -> Tuple[List, List, Tuple]:
    # Create a GeoDataFrame from the GeoJSON
    gdf = gpd.GeoDataFrame.from_features(geojson_data)

    # Initialize southwest, northeast, and center coordinates
    southwest = [float('inf'), float('inf')]  # Initialize with high values
    northeast = [float('-inf'), float('-inf')]  # Initialize with low values
    center = [None, None]

    for feature in gdf.itertuples():
        # Extract geometry (assuming MultiPolygon type)
        geometry = feature.geometry

        if geometry.geom_type == 'MultiPolygon':
            # Iterate through each polygon in the MultiPolygon
            for polygon in geometry.geoms:
                coords = polygon.exterior.coords.xy

                # Update southwest and northeast corners (lon, lat order)
                southwest[1] = min(southwest[1], min(coords[0]))
                southwest[0] = min(southwest[0], min(coords[1]))
                northeast[1] = max(northeast[1], max(coords[0]))
                northeast[0] = max(northeast[0], max(coords[1]))

        # Calculate center point (assuming centroid)
        if geometry is not None:
            center = geometry.centroid.xy

    return southwest, northeast, (center[1], center[0])


def filter_geojson(trips_df: pd.DataFrame) -> dict:
    aux_geojson = {"type": "FeatureCollection"}
    geojson_features = json.load(open(str(pathlib.Path(__file__).absolute().parent.parent / 'countries.geojson')))['features']
    # Filter geojson data based in countries
    aux_geojson['features'] = [data for data in geojson_features if data['properties']['ADMIN'] in trips_df['country'].unique()]
    return aux_geojson


def display_map(trips_df: pd.DataFrame) -> str:
    # Filter to optimize app
    geojson_data = filter_geojson(trips_df)

    # Get map corners and center coordinates
    southwest, northeast, center = calculate_sw_ne_c_coordinates(geojson_data)
    # Create tuple for Folium
    center_tuple = tuple(float(x[0]) for x in center)

    # Create the map canvas
    f_map = folium.Map(location=center_tuple, tiles='CartoDB Positron')
    f_map.fit_bounds([southwest, northeast])

    # Add countries boundaries data
    # country_fill_color = random.choice(['BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'RdPu', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'])
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        data=trips_df,
        columns=['country', 'days'],
        key_on='feature.properties.ADMIN',
        line_opacity=0.8,
        fill_opacity=0.8,
        fill_color='GnBu',
        highlight=True)
    choropleth.geojson.add_to(f_map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['ADMIN'],  #, 'trips'],
                                       labels=False)
    )
    # folium.plugins.MousePosition(position='topleft', separator=' | ', prefix="Mouse Position:").add_to(f_map)
    st_map = st_folium(f_map, width=1050, height=625)

    # Check for clicked country
    last_country_clicked = st_map['last_active_drawing']['properties']['ADMIN'] if st_map['last_active_drawing'] else ''
    return last_country_clicked

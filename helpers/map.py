import folium
import pandas as pd
from streamlit_folium import st_folium
import pathlib
import json


def map_data(trips_df: pd.DataFrame):
    geojson = json.load(open(str(pathlib.Path(__file__).absolute().parent.parent / 'countries.geojson')))['features']
    countries_boundaries = [{
        'country': data['properties']['ADMIN'],
        'coordinates': data['geometry']['coordinates'][0][0]
    } for data in geojson]
    coordinates_df = pd.DataFrame.from_records(countries_boundaries)
    df = trips_df.merge(coordinates_df, how='left', on='country')


def display_map(trips_df: pd.DataFrame):
    # Get map data (coordinates and zoom)
    map_data(trips_df)

    # Create the map canvas
    f_map = folium.Map(location=[35, 3], zoom_start=2, tiles='CartoDB positron')

    # Add countries boundaries data
    choropleth = folium.Choropleth(
        geo_data=str(pathlib.Path(__file__).absolute().parent.parent / 'countries.geojson'),
        data=trips_df,
        columns=('country', 'days'),
        key_on='features.properties.ADMIN',
        line_opacity=0.8,
        highlight=True)
    choropleth.geojson.add_to(f_map)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['ADMIN'],
                                       labels=False)
    )

    st_map = st_folium(f_map, width=1050, height=625)


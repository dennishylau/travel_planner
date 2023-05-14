# %%
import streamlit as st
import pandas as pd
import gspread
import googlemaps
from utils import (fetch_gmaps_data,
                   plot_poi,
                   plot_intra_city)
from collections import namedtuple
import osmnx as ox
from streamlit_folium import st_folium
from streamlit_javascript import st_javascript as st_js

# %%
# configuration
ox.settings.log_console = True
ox.settings.use_cache = True
st.set_page_config(page_title='Travel Planner POC', layout="wide")
st.title('2023-09 Japan')
# get gsheet as datasource
gc = gspread.service_account_from_dict(st.secrets.google_secrets)
sh = gc.open_by_key(st.secrets["gsheet_key"])
ws = sh.worksheet("main")
gs_df = pd.DataFrame(ws.get_all_records())
# dynamically declare the Place type
Place = namedtuple('Place', gs_df.dtypes.index.tolist())
# fetch gmaps data into df and update gsheet if missing
gmaps = googlemaps.Client(key=st.secrets["gmaps_api_key"])
fetch_gmaps_data(gs_df, gmaps, ws)
# sidebar
travel_dates = sorted(gs_df['date'].unique())
with st.sidebar:
    input_date = st.selectbox('Select Travel Date', ['All'] + travel_dates)
# UI element calculation
screen_width = st_js("window.innerWidth")
map_width = screen_width - 50
map_height = 400 if screen_width < 768 else 650


def plot_date(gs_df: pd.DataFrame, date_str: str):
    st.header(f'{date_str}')

    date_df = gs_df.query(f"date == '{date_str}'")
    places = [Place(*date_df.loc[idx, :]) for idx, row in date_df.iterrows()]

    # TODO: update the hardcoded country
    country = 'Japan'

    for city in date_df['city'].unique():
        st.subheader(f'City: {city}')
        date_city_df = date_df.query(f"city == '{city}'")
        st.dataframe(date_city_df)
        pois = [i for i in places if i.city == city]
        if len(pois) == 0:
            break
        elif len(pois) == 1:
            interactive_map = plot_poi(pois[0])
        else:
            interactive_map = plot_intra_city(country, pois)
        st_folium(interactive_map,
                  width=map_width,
                  height=map_height,
                  returned_objects=[])


# %%
plotted_dates = travel_dates if input_date == 'All' else [input_date]
for date in plotted_dates:
    plot_date(gs_df, date)

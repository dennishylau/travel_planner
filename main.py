# %%
import streamlit as st
import pandas as pd
import gspread
from utils import (
    fetch_gmaps_data,
    update_ws,
    plot_date,
    build_aggrid,
    update_date_order)
from collections import namedtuple
import osmnx as ox

from streamlit_javascript import st_javascript as st_js
# %%
# configuration
ox.settings.log_console = True
ox.settings.use_cache = True
st.set_page_config(page_title='Travel Planner POC', layout="wide")
st.header('2023-09 Japan')
# get gsheet as datasource
gc = gspread.service_account_from_dict(st.secrets.google_secrets)
sh = gc.open_by_key(st.secrets["gsheet_key"])
ws = sh.worksheet("main")
gs_df = pd.DataFrame(ws.get_all_records())
gs_df.sort_values(by=['date', 'date_order'], na_position='last', inplace=True)
# dynamically declare the Place type
Place = namedtuple('Place', gs_df.dtypes.index.tolist())
# fetch gmaps data into df and update gsheet if missing
fetch_gmaps_data(gs_df, ws)
travel_dates = sorted(gs_df['date'].unique())
# UI element calculation
screen_width = st_js("window.innerWidth")
is_mobile = True if screen_width < 768 else False
map_width = screen_width - 50 if is_mobile else screen_width / 2
map_height = 400 if is_mobile else 650
# UI cols
col1, col2 = st.columns([1, 1], gap='large')


with col1:
    input_date = st.selectbox('Select Travel Date', ['All'] + travel_dates)
    plotted_dates = travel_dates if input_date == 'All' else [input_date]
    for date in plotted_dates:
        plot_date(gs_df, date, map_width, map_height)


if not is_mobile:
    with col2:
        # reload_data = False
        grid = build_aggrid(gs_df)
        gs_df = grid['data']
        updated = update_date_order(gs_df, travel_dates)
        if updated:
            update_ws(ws, gs_df)


st.write('''
Data source: https://docs.google.com/spreadsheets/d/1glRBcB2xiCkkUFF2Xq_sslf8wP_aNpOG0RWWHbu228A/edit#gid=0
''')

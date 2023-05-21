import streamlit as st
import pandas as pd
import gspread
import googlemaps

GMAPS_CLIENT = googlemaps.Client(key=st.secrets["gmaps_api_key"])


def update_ws(ws: gspread.Worksheet, df: pd.DataFrame):
    with st.spinner('Updating Google Sheet'):
        ws.update([df.columns.values.tolist()] + df.values.tolist())


def fetch_gmaps_data(gs_df: pd.DataFrame,
                     ws: gspread.Worksheet,
                     gmaps: googlemaps.Client = GMAPS_CLIENT) -> pd.DataFrame:
    '''
    Fetch missing gmaps data for google sheet records
    gs_df: the travel planner dataframe
    ws: the gspread worksheet object
    '''

    updated = False

    for idx, row in gs_df.iterrows():
        if row['place_id'].strip() == "" and row['name'].strip() != "" and row['city'].strip() != "":
            updated = True
            print(f"Updating row: {row['name']}")
            geocode_results = gmaps.geocode(f"{row['name']}, {row['city']}")
            if len(geocode_results) == 0:
                break
            result = geocode_results[0]
            gs_df.at[idx, 'place_id'] = result["place_id"]
            gs_df.at[idx, 'formatted_address'] = result["formatted_address"]
            gs_df.at[idx, 'lat'] = result['geometry']["location"]['lat']
            gs_df.at[idx, 'long'] = result['geometry']["location"]['lng']

    # %%
    if updated:
        update_ws(ws, gs_df)

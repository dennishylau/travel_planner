import streamlit as st
import pandas as pd
from utils import (
    plot_poi,
    plot_intra_city,
)
from streamlit_folium import st_folium
from collections import namedtuple


def plot_date(
        gs_df: pd.DataFrame,
        date_str: str,
        width: int = None,
        height: int = None):

    Place = namedtuple('Place', gs_df.dtypes.index.tolist())

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
                  width=width,
                  height=height,
                  returned_objects=[])

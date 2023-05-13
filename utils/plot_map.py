import folium
import osmnx as ox
from .osmnx import get_region_graph
from .route import route_intra_city
from .folium import add_marker
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Place


def plot_poi(poi: 'Place') -> folium.Map:
    interactive_map = folium.Map(
        location=(poi.lat, poi.long),
        zoom_start=17,
        scrollWheelZoom=False)
    add_marker(interactive_map, 0, poi)
    return interactive_map


def plot_intra_city(country: str, pois: list['Place']) -> folium.Map:
    city = pois[0].city
    graph = get_region_graph(f'{city}, {country}')
    route = route_intra_city(graph, pois)
    interactive_map = ox.plot_route_folium(
        graph,
        route,
        route_map=folium.Map(scrollWheelZoom=False),
        tiles='openstreetmap',  # use for hd map
        weight=5
    )
    interactive_map.scrollWheelZoom = False
    for i in range(len(pois)):
        add_marker(interactive_map, i, pois[i])
    return interactive_map

import streamlit as st
import osmnx as ox
import networkx as nx
from enum import Enum, auto
from networkx import Graph
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Place

ox.settings.log_console = True
ox.settings.use_cache = True


class TransportMode(str, Enum):
    walk = auto()
    drive = auto()
    bike = auto()


class OptimizeMode(str, Enum):
    length = auto()
    time = auto()


@st.cache_data(persist=True)
def get_region_graph(osmnx_place: str,
                     network_type: TransportMode = TransportMode.walk) -> Graph:
    '''
    osmnx_place: place like 'Osaka, Japan'
    '''
    graph = ox.graph_from_place(osmnx_place, network_type=network_type.name)
    return graph


def get_shortest_route(graph: Graph,
                       src: 'Place',
                       dst: 'Place',
                       optimizer: OptimizeMode = OptimizeMode.time):
    # create graph from OSM within the boundaries of some
    # geocodable place(s)
    # find the nearest node to the start location
    orig_node = ox.distance.nearest_nodes(graph, src.long,
                                          src.lat)
    # find the nearest node to the end location
    dest_node = ox.distance.nearest_nodes(graph, dst.long,
                                          dst.lat)
    #  find the shortest path
    shortest_route = nx.shortest_path(graph,
                                      orig_node,
                                      dest_node,
                                      weight=optimizer.name)
    return graph, shortest_route

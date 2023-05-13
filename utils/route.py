from networkx import Graph
from .osmnx import get_shortest_route
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Place


def route_intra_city(graph: Graph, places: list['Place']) -> list[float]:
    shortest_route = []
    if len(places) < 1:
        raise Exception('Cannot plot single point route.')

    if len(set([i.city for i in places])) > 1:
        raise Exception('Cannot plot multicity route.')

    for idx in range(0, len(places) - 1):
        src = places[idx]
        dst = places[idx + 1]
        route = get_shortest_route(graph, src, dst)
        shortest_route += route[1]

    return shortest_route

import folium
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Place


def add_marker(map: folium.Map, idx: int, poi: 'Place'):
    marker = folium.Marker(
        location=(poi.lat, poi.long),
        tooltip=f'{idx + 1} - {poi.name}',
        popup=f'<a href=https://www.google.com/maps/search/?api=1&query={poi.name},%20{poi.city}&query_place_id={poi.place_id}>Open GMaps</a>',
        icon=folium.Icon(icon='cutlery', color='blue'))
    marker.add_to(map)

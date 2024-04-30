import geopandas
import pandas
import folium
import shapely
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_tooltip(row):
    party_names = dane.columns[4:]
    party_data = {party: row[party] for party in party_names}
    sorted_parties = sorted([(party, seats) for party, seats in party_data.items() if seats > 0], key=lambda x: x[1], reverse=True)
    return '<br>'.join([f"{party}: {seats}" for party, seats in sorted_parties])

wojewodztwa = geopandas.read_file('wojewodztwa-max.geojson')
wojewodztwa = wojewodztwa.sort_values(by="nazwa")
wojewodztwa = wojewodztwa.set_index('nazwa')
dane = pandas.read_csv('nauka_map.csv', delimiter=";")
wojewodztwa_z_danymi = wojewodztwa.merge(dane, on='nazwa')
wojewodztwa_z_danymi['color'] = wojewodztwa_z_danymi.apply(lambda row: 'orange' if row['Koalicja'] > row['Opozycja'] else ('blue' if row['Koalicja'] < row['Opozycja'] else 'grey'), axis=1)
wojewodztwa_z_danymi['tooltip'] = wojewodztwa_z_danymi.apply(create_tooltip, axis=1)
m = folium.Map(location=[52, 19], zoom_start=6, zoom_control=False, min_zoom=6, max_zoom=6 ,
    scrollWheelZoom=False,
    dragging=False,)
m.options['doubleClickZoom'] = False

folium.GeoJson(
    wojewodztwa_z_danymi,
    style_function=lambda feature: {
        'fillColor': 'orange' if feature['properties']['color'] == 'orange' else ('blue' if feature['properties']['color'] == 'blue' else 'grey'),
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    },
    highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.7},
    tooltip=folium.GeoJsonTooltip(fields=['tooltip'],
        aliases=[''],
        labels=False,
        localize=True,
        style=("font-size: 12px; font-weight: bold;")),).add_to(m)
m.save('map.html')
m.show_in_browser()

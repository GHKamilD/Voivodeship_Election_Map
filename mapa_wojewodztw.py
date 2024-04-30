import geopandas
import pandas
import folium
import shapely
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_tooltip(row):
    # Extract relevant data and sort it
    party_data = {party: row[party] for party in ['PiS', 'KO', 'TD', 'Lewica', 'Konf', 'BS', 'OKS', 'SS']}
    sorted_parties = sorted([(party, seats) for party, seats in party_data.items() if seats > 0], key=lambda x: x[1], reverse=True)
    # Format the tooltip string
    return '<br>'.join([f"{party}: {seats}" for party, seats in sorted_parties])

wojewodztwa = geopandas.read_file('wojewodztwa-max.geojson')
wojewodztwa = wojewodztwa.sort_values(by="nazwa")
wojewodztwa = wojewodztwa.set_index('nazwa')
dane = pandas.read_csv('nauka_map.csv', delimiter=";")
wojewodztwa_z_danymi = wojewodztwa.merge(dane, on='nazwa')
wojewodztwa_z_danymi['color'] = wojewodztwa_z_danymi.apply(lambda row: 'orange' if row['Koalicja'] > row['Opozycja'] else ('blue' if row['Koalicja'] < row['Opozycja'] else 'grey'), axis=1)
wojewodztwa_z_danymi['tooltip'] = wojewodztwa_z_danymi.apply(create_tooltip, axis=1)
print(wojewodztwa_z_danymi['tooltip'])
"""fig, ax = plt.subplots(figsize=(10, 8))
wojewodztwa_z_danymi.plot(ax=ax, color=wojewodztwa_z_danymi['color'], edgecolor='black', legend=True)
ax.set_axis_off()
orange_patch = mpatches.Patch(color='orange', label='Koalicja')
blue_patch = mpatches.Patch(color='blue', label='Opozycja')
legend = ax.legend(handles=[orange_patch, blue_patch], loc='center left', bbox_to_anchor=(1.05, 0.5))"""
"""m = wojewodztwa_z_danymi.explore(
    column='color',
    color = 'color',
    tooltip=['nazwa'],
    popup=True,
    tiles='CartoDB positron',
    cmap='Set1',
    style_kwds=dict(color='black')
)
m.save('map.html')
m"""
m = folium.Map(location=[52, 19], zoom_start=6, zoom_control=False,
    scrollWheelZoom=False,
    dragging=False,)

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
        labels=True,
        localize=True,
        style=("font-size: 12px; font-weight: bold;")),).add_to(m)
#m.save('map.html')
m.show_in_browser()
#merged_df.plot(cmap='RdYlBu', categorical=True, column='color', legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
#ax.legend(['orange', 'blue'], ['Koalicja', 'Opozycja'], loc='center')
"""fig, ax = plt.subplots()
patches = ax.get_legend_handles_labels()

wojewodztwa_z_danymi.plot(column='color', cmap='RdYlBu', ax=ax, legend=True)
ax.set_title('Polish Voivodeships by Koalicja and Opozycja')"""
#plt.show()
#print(merged_df["Miejsca"])
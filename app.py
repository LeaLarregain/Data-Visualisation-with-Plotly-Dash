import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies

app = Dash(__name__)

# 1 - Create some graph for RATP dataset

df = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
sorted_df = df.sort_values(by=['Trafic'], ascending=False)
topBar = sorted_df.groupby('Réseau').head(5)
topPie = df.head(20)

# 2 - Create some graph for IDF dataset
df2 = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')

exploit_counts = df2.groupby('exploitant')['nom'].count().reset_index()
station_counts = df2.groupby('ligne')['nom'].count().reset_index()

df2[['lat', 'lng']] = df2['Geo Point'].str.split(',', expand=True)
df2['lat'] = df2['lat'].str.strip().astype(float)
df2['lng'] = df2['lng'].str.strip().astype(float)

app.layout = html.Div(children=[
    # Create a bar chart that represents the TOP 10 stations with the biggest traffic
    html.H1("RATP & IDF : Stations visualization", style={'text-align': 'center'}),
    html.H2("TOP 10 of the station with the biggest traffic and pie chart that represents trafic per cities",
            style={'color': '#000080', 'text-decoration': 'underline'}),
    dcc.Dropdown(
        id='reseau-filter',
        options=[{'label': category, 'value': category} for category in sorted_df['Réseau'].unique()],
        value=None,
        placeholder='Select a reseau'
    ),
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(topBar, x='Station', y='Trafic'),
        style={'width': '50%', 'align': 'right', 'display': 'inline-block'}
    ),
    # Create a Pie chart that represents trafic per cities (to make it clear, you can take only the TOP 5)
    dcc.Graph(
        id='pie-chart',
        figure=px.pie(topPie, values='Trafic', names='Ville'),
        # Organize those two chart on the same row (they have to be side by side)
        style={'width': '50%', 'align': 'right', 'display': 'inline-block'}
    ),
    # Create a bar chart that represents the number of stations per exploitant
    html.H2("Bar chart that represents the number of Stations per Exploitant",
            style={'color': '#000080', 'text-decoration': 'underline'}),
    dcc.Dropdown(
        id='exploitant-filter',
        options=[{'label': category, 'value': category} for category in df2['exploitant'].unique()],
        value=None,
        placeholder='Select an exploitant'
    ),
    dcc.Graph(
        id='bar-chart2',
        figure=px.bar(exploit_counts, x='exploitant', y='nom')
    ),
    # Create a chart that represents the number of stations per Ligne
    html.H2("Chart that represents the number of Stations per ligne",
            style={'color': '#000080', 'text-decoration': 'underline'}),

    dcc.Graph(
        id='bar-chart3',
        figure=px.bar(station_counts, x='ligne', y='nom',
                      labels={'ligne': 'Ligne', 'nom': 'Number of stations'})
    ),
    html.H2("Position of the stations", style={'color': '#000080', 'text-decoration': 'underline'}),
    dcc.Graph(id="map-graph", figure=px.scatter_mapbox(
        df2,
        lat='lat',
        lon='lng',
        hover_name='nom',
        zoom=6,
        color="exploitant",
        labels={'exploitant':'Exploitant', 'lat':'Latitude', 'lng':'Longitude'}
    ).update_layout(mapbox_style='open-street-map'))
])


@app.callback(
    dependencies.Output('bar-chart', 'figure'),
    dependencies.Input('reseau-filter', 'value')
)
def update_bar_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = topBar
    else:
        # Filter the df based on selection
        filtered_df = topBar[topBar['Réseau'] == category]

    return px.bar(filtered_df, x='Station', y='Trafic', labels={'Station':'Station', 'Trafic':'Trafic'})

@app.callback(
    dependencies.Output('pie-chart', 'figure'),
    dependencies.Input('reseau-filter', 'value')
)
def update_pie_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = topPie
    else:
        # Filter the df based on selection
        filtered_df = df[df['Réseau'] == category].groupby('Ville').sum().sort_values(by=['Trafic'],
                                                                                      ascending=False).head(5).reset_index()
    return px.pie(filtered_df, values='Trafic', names='Ville')



@app.callback(
    dependencies.Output('bar-chart2', 'figure'),
    dependencies.Input('exploitant-filter', 'value')
)
def update_bar_chart2(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = exploit_counts
    else:
        # Filter the df based on selection
        filtered_df = exploit_counts[exploit_counts['exploitant'] == category]

    return px.bar(filtered_df, x='exploitant', y='nom', labels={'exploitant':'Exploitant', 'nom':'Number of stations'})

@app.callback(
    dependencies.Output('bar-chart3', 'figure'),
    dependencies.Input('exploitant-filter', 'value')
)
def update_bar_chart2(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = station_counts
    else:
        # Filter the df based on selection
        filtered_df = df2[df2['exploitant'] == category].groupby('ligne')['nom'].count().reset_index()

    return px.bar(filtered_df, x='ligne', y='nom', labels={'ligne':'Ligne', 'nom':'Number of stations'})


# Run the script.
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
    #If you want to run app.py on your localhost :
    #app.run_server(debug=True)

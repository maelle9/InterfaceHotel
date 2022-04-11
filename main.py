import sys
import numpy as np
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# load df to print graph
df_total = pd.read_csv("stat.csv", sep=";")
fig = px.line(df_total, x="date", y="mean")

df = pd.read_csv("test_carte.csv", sep=";")
stars_choice = df['stars'].unique()
stars_choice = np.insert(stars_choice,0,10)
date_choice = df['start_date'].unique()
date_choice = np.insert(date_choice,0,'all')
adulte_choice = df['nb_adulte'].unique()
adulte_choice = np.insert(adulte_choice,0,10)
enfant_choice = df['nb_enfant'].unique()
enfant_choice = np.insert(enfant_choice,0,10)
room_choice = df['nb_chambre'].unique()
room_choice = np.insert(room_choice,0,10)
df = df.drop(['gps','nb_adulte','nb_enfant','nb_chambre'], axis=1)

# Load data
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])  # initialisation du dash app

# propriétés des onglets

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    if sys.version_info < (3, 0):  # Pandas 1.0.0 does not support Python 2
        return 'any'

    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        return 'any'
#On ajoute un layout sur la page
table = dash_table.DataTable( id = 'table_data',
                              columns=[{'name': i, 'id': i, 'type': table_type(df[i])} for i in df.columns],
                              sort_action = "native",
                              sort_mode= "multi",
                              css = [{
                                  'selector': 'table',
                                  'rule': 'table-layout: fixed'  # note - this does not work with fixed_rows
                              }],
                              style_table = {'height': 400},
                              style_data =  {
                                 'width': '{}%'.format(100. / len(df.columns)),
                                 'textOverflow': 'hidden'
                             })


tab1 = html.Div([ html.H3('Accueil'),
            html.Div([
                html.P('Projet de Clément REIFFERS, Quentin MOREL, Maëlle MARCELIN, Adrien TIRLEMONT'),
                html.P("Récupération de données d'hôtel et analyse "),
                html.Div([
                    dcc.Dropdown(
                        id='stars',
                        options=[{'label': i, 'value': i} for i in stars_choice],
                        value=10
                    ),
                    dcc.Dropdown(
                        id='date',
                        options=[{'label': i, 'value': i} for i in date_choice],
                        value="all"
                    ),
                    dcc.Dropdown(
                        id='nb_adulte',
                        options=[{'label': i, 'value': i} for i in adulte_choice],
                        value=10
                    ),
                    dcc.Dropdown(
                        id='nb_enfant',
                        options=[{'label': i, 'value': i} for i in enfant_choice],
                        value=10
                    ),
                    dcc.Dropdown(
                        id='nb_room',
                        options=[{'label': i, 'value': i} for i in room_choice],
                        value=10
                    ),
                ],style={'width': '10%'})
            ])
])

app.layout = html.Div([
    html.H1('Hotel'),
    dcc.Tabs(id="tabs-hotel", value='tab-1-accueil', children=[
        dcc.Tab(label='Accueil', value='tab-1-accueil',style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
            tab1,
            table
            ])
        ]),
        dcc.Tab(label='Statistique', value='tab-2-statistique', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                html.H3('Statistique'),
                dcc.Graph(
                    id='stat-2',
                    figure=fig
            )
        ])
        ]),
        dcc.Tab(label='Carte', value='tab-3-carte',style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                        html.H3('Carte'),
                        html.Div([
                            html.Iframe(id='map', srcDoc=open('Carte_hotel.html', 'r').read(), width='80%', height='500vh')

                        ], style={'padding': 50})
                    ])
        ])
    ], style=tabs_styles),
    html.Div(id='tabs-content-hotel')

])


def update(stars_choice,date_choice,adulte_choice,enfant_choice,room_choice):
    df = pd.read_csv("test_carte.csv", sep=";")
    df = df.drop(['gps'], axis=1)
    if stars_choice == 10:
        df = df
    else:
        df = df[(df['stars']==stars_choice)]
    if date_choice == "all" :
        df = df
    else:
        df = df[(df['start_date']==date_choice)]
    if adulte_choice == 10:
        df = df
    else:
        df = df[(df['nb_adulte']==adulte_choice)]
    if enfant_choice ==10:
        df = df
    else:
        df = df[(df['nb_enfant']==enfant_choice)]
    if room_choice == 10:
        df = df
    else:
        df = df[(df['nb_chambre']==room_choice)]
    df = df.drop(['nb_adulte','nb_enfant','nb_chambre'], axis=1)
    data=df.to_dict('records')
    return data

@app.callback(Output('table_data', 'data'),
              [Input('stars', 'value'),
               Input('date', 'value'),
               Input('nb_adulte', 'value'),
               Input('nb_enfant', 'value'),
               Input('nb_room', 'value')
               ])
def render_content(stars,date,nb_adulte,nb_enfant,nb_room):
    table = update(stars, date, nb_adulte, nb_enfant, nb_room)
    return table



if __name__ == '__main__':
    app.run_server(debug=True)

import sys
from dash import dash_table, html, dcc
import pandas as pd
import columns


stars_choice,date_choice,adulte_choice,enfant_choice,room_choice,lenght = columns.columns()

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

df = pd.read_csv("test_carte.csv", sep=";")
df_col = df.drop(['gps','nb_adulte','nb_enfant','nb_chambre'], axis=1)
table = dash_table.DataTable( id = 'table_data',
                              columns=[{'name': i, 'id': i, 'type': table_type(df_col[i])} for i in df_col.columns],
                              sort_action = "native",
                              sort_mode= "multi",
                              css = [{
                                  'selector': 'table',
                                  'rule': 'table-layout: fixed'  # note - this does not work with fixed_rows
                              }],
                              style_table = {'height': 400},
                              style_data =  {
                                 'width': '{}%'.format(100. / lenght),
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
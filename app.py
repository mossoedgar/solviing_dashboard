# For creating an executable, view this site:
#   https://community.plotly.com/t/convert-dash-to-executable-file-exe/14222/3
#   coding: utf-8
#   Import needed libraries
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# import the necessaries libraries
from plotly import express as px
from plotly import offline as py
from plotly.graph_objs import Scatter, Layout

# import graph_objects from plotly package
from plotly import graph_objects as go

# import make_subplots function from plotly.subplotsto make grid of plots
from plotly.subplots import make_subplots

from sqlFunctions import queryTable

import webbrowser
from threading import Timer


port = 5000

def open_browser():
        webbrowser.open_new("http://localhost:{}".format(port))


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


def clean_treated_data(df):
    if 'clave_entidad_federativa' in df.columns:
        df = df[~df['clave_entidad_federativa'].isna()]
        df['clave_entidad_federativa'] = df['clave_entidad_federativa'].astype(str)
        df = df[pd.to_numeric(df['clave_entidad_federativa'], errors='coerce').notnull()]
        #df = df.loc[df.SUPERFICIE_VENDIBLE.str.isnumeric()]
        df['clave_entidad_federativa'] = df['clave_entidad_federativa'].astype(int)
    if 'clave_municipio' in df.columns:
        df = df[~df['clave_municipio'].isna()]
        df['clave_municipio'] = df['clave_municipio'].astype(str)
        df = df[pd.to_numeric(df['clave_municipio'], errors='coerce').notnull()]
        #df = df.loc[df.SUPERFICIE_VENDIBLE.str.isnumeric()]
        df['clave_municipio'] = df['clave_municipio'].astype(int)

    if 'valor_mun_total_promedio' in df.columns:
        df['valor_mun_total_promedio'] = df['valor_mun_total_promedio'].astype(float)
        df['valor_mun_total_promedio'] = df['valor_mun_total_promedio'].round(2)

    if 'valor_mun_m2_promedio' in df.columns:
        df['valor_mun_m2_promedio'] = df['valor_mun_m2_promedio'].astype(float)
        df['valor_mun_m2_promedio'] = df['valor_mun_m2_promedio'].round(2)

    return df

def cleanFigureData(df):

    df['fecha'] = df['fecha'].astype(str)
    df['fecha'] = [x[:4] + ' ' + x[4:] for x in df['fecha']]

    if 'clave_entidad_federativa' in df.columns:
        df = df[~df['clave_entidad_federativa'].isna()]
        df['clave_entidad_federativa'] = df['clave_entidad_federativa'].astype(str)
        df = df[pd.to_numeric(df['clave_entidad_federativa'], errors='coerce').notnull()]
        #df = df.loc[df.SUPERFICIE_VENDIBLE.str.isnumeric()]
        df['clave_entidad_federativa'] = df['clave_entidad_federativa'].astype(int)
    if 'clave_municipio' in df.columns:
        df = df[~df['clave_municipio'].isna()]
        df['clave_municipio'] = df['clave_municipio'].astype(str)
        df = df[pd.to_numeric(df['clave_municipio'], errors='coerce').notnull()]
        #df = df.loc[df.SUPERFICIE_VENDIBLE.str.isnumeric()]
        df['clave_municipio'] = df['clave_municipio'].astype(int)

    if 'valor_mun_total_promedio' in df.columns:
        df['valor_mun_total_promedio'] = df['valor_mun_total_promedio'].astype(float)
        df['valor_mun_total_promedio'] = df['valor_mun_total_promedio'].round(2)

    if 'valor_mun_m2_promedio' in df.columns:
        df['valor_mun_m2_promedio'] = df['valor_mun_m2_promedio'].astype(float)
        df['valor_mun_m2_promedio'] = df['valor_mun_m2_promedio'].round(2)

    return df

#df_average_prices_complete = pd.read_excel('C:/Users/edgar/Documents/PythonScripts/Solviing/dashboard_historicos/promedio_valuaciones_estado_mun_final.xlsx')
#df = df_average_prices_complete
#df = clean_treated_data(df)

query = '''
    SELECT
    *
    FROM precios_promedio_dashboard
'''
df = queryTable(query)

df_filt = df[['entidad_federativa', 'municipio']]
df_test = df_filt.groupby(['entidad_federativa','municipio']).count().reset_index()
options_dict = df_test.groupby('entidad_federativa')['municipio'].agg(list).to_dict()

##############################################################################################################################

app = dash.Dash(__name__, assets_folder=find_data_file('./assets/'))

server = app.server

app.layout = html.Div(id = 'parent', children = [
                html.H1(id = 'H1',
                        children = 'Dashboard Demográfico de México',
                        style = {'textAlign':'center',
                                'marginTop':40,
                                'marginBottom':40
                                }
                        ),
                html.Div([

                    html.Div([
                        dcc.Dropdown(
                            list(options_dict.keys()),
                            'Ciudad de México',
                            id='dropdown-estado'
                        )
                    ], style={'width': '25%', 'display': 'inline-block'}),

                    html.Div([
                        dcc.Dropdown(
                            #df['municipio'].unique(),
                            #'Selecciona un Municipio',
                            id = 'dropdown-municipio'
                            #options=[
                            #    {'label': i, 'value': i} for i in df.municipio.unique()
                            #],
                            #multi=False,
                            #placeholder='Filtro por municipio...'
                        )#,
                        #dcc.Store(id='dropdown-municipio')
                    ], style={'width': '25%', 'float': 'right', 'display': 'inline-block'})
                ]),
                html.Div([
                    dcc.Graph(id = 'valor-inmueble'),
                    dcc.Graph(id = 'valor-inmueble-m2')
                ]),
                html.Div([
                    dcc.Store(id='dff_estado'),
                    dcc.Store(id='dff_filtered'),
                ])
            ])


##########################################################################   SELECCION ESTADO Y MUNICIPIO   ##########################################################################
################################################### OPCIONES PARA MUNICIPIO ###################################################
@app.callback(Output('dropdown-municipio', 'options'),
              Input('dropdown-estado', 'value')
)

def set_municipio_options(estado):
    return [{'label': i, 'value': i} for i in options_dict[estado]]

################################################### OPCION SELECCIONADA PARA MUNICIPIO ###################################################

@app.callback(Output('dropdown-municipio', 'value'),
              Input('dropdown-municipio', 'options')
)

def set_municipio_value(available_options):
    return available_options[0]['value']

################################################### FILTRO DE DATOS POR ESTADO Y MUNICIPIO ###################################################

@app.callback(Output('dff_filtered', 'data'),
              Input('dropdown-estado', 'value'),
              Input('dropdown-municipio', 'value')
)

def filter_df(estado, municipio):

    #df = df_average_prices_complete
    #df = clean_treated_data(df)
    dff = df[(df['entidad_federativa'] == str(estado)) & (df['municipio'] == str(municipio))]

    return dff.to_json(date_format='iso', orient='split')


##########################################################################  FIG VALORINMUEBLE    ##########################################################################


@app.callback(Output(component_id='valor-inmueble', component_property= 'figure'),
              Input(component_id='dff_filtered', component_property= 'data')
)

def update_graph(dff_filtered):

    if dff_filtered is None:

        raise PreventUpdate

    else:

        dff = pd.read_json(dff_filtered, orient='split')
        dff = cleanFigureData(dff)
        dff['valor_mun_total_promedio_porcentaje'] = (dff['valor_mun_total_promedio'].pct_change())*100
        dff['valor_mun_total_promedio_porcentaje'] = dff['valor_mun_total_promedio_porcentaje'].round(2)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=dff.fecha,
            y=dff.valor_mun_total_promedio,
            text = dff.valor_mun_total_promedio,
            textposition = "auto",
            textfont=dict(
                family="Helvetica",
                size=12,
                color="#ebebeb"
            ),
            hovertemplate="Valor Promedio Inmueble ($MXN)<br>Trimestre=%{x}<br>Valor=%{y}<extra></extra>",
            name="Valor Promedio Inmueble",
            yaxis="y1"
        ))

        fig.add_trace(go.Scatter(
            x = dff.fecha,
            y = dff.valor_mun_total_promedio_porcentaje,
            mode="lines+markers+text",
            text = dff.valor_mun_total_promedio_porcentaje,
            textposition = "top center",
            textfont=dict(
                family="Helvetica",
                size=14,
                color="#f78e43"
            ),
            hovertemplate="Delta V.P. Inmueble (%)<br>Trimestre=%{x}<br>Valor=%%{y}<extra></extra>",
            name = "Delta V.P. Inmueble (%)",
            yaxis = "y2"
        ))

        # fig.update_layout(hovermode='x unified')
        fig.add_trace(go.Scatter(
            x=dff.fecha,
            y=dff.valor_mun_total_promedio,
            mode = 'lines',
            marker_color='black',
            hovertemplate="Tendencia V.P. Inmueble ($MXN)<br>Trimestral=%{x}<br>Valor=%{y}<extra></extra>",
            name='Tendencia V.P. Inmueble',
            yaxis="y1"
        ))

        fig.update_layout(
            # split the x-axis to fraction of plots in
            # proportions
            xaxis=dict(
                    domain=[0.05, 0.95]
                ),

            # pass the y-axis title, titlefont, color
            # and tickfont as a dictionary and store
            # it an variable yaxis
            yaxis=dict(
                title="Valor Promedio Inmueble ($MXN)",
                titlefont=dict(
                    color="#0000ff"
                ),
                tickfont=dict(
                    color="#0000ff"
                )
            ),

            # pass the y-axis 2 title, titlefont, color and
            # tickfont as a dictionary and store it an
            # variable yaxis 2
            yaxis2=dict(
                title="Delta V.P. Inmueble (%)",
                titlefont=dict(
                    color="#FF0000"
                ),
                tickfont=dict(
                    color="#FF0000"
                ),
                anchor="free",  # specifying x - axis has to be the fixed
                overlaying="y",  # specifyinfg y - axis has to be separated
                side="right",  # specifying the side the axis should be present
                position=0.95
            )

        )

        fig.update_layout(
            title_text="Valor de inmuebles y m2 en México (2019 - 2020)",
            title_x=0.5,
            xaxis_title="Trimestre (formato: año trimestre)",
        )


        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, hovermode='x')

        fig['layout']['yaxis'].update(autorange = True)

        fig.update_layout(transition_duration=500)#, hovermode='x')

        return fig

##########################################################################   FIG INMUEBLE M2    ##########################################################################

@app.callback(Output(component_id='valor-inmueble-m2', component_property= 'figure'),
              Input(component_id='dff_filtered', component_property= 'data')
)

def update_graph(dff_filtered):

    if dff_filtered is None:

        raise PreventUpdate

    else:

        dff = pd.read_json(dff_filtered, orient='split')
        dff = cleanFigureData(dff)
        dff['valor_mun_m2_promedio_porcentaje'] = (dff['valor_mun_m2_promedio'].pct_change())*100
        dff['valor_mun_m2_promedio_porcentaje'] = dff['valor_mun_m2_promedio_porcentaje'].round(2)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=dff.fecha,
            y=dff.valor_mun_m2_promedio,
            text = dff.valor_mun_m2_promedio,
            textposition = "auto",
            textfont=dict(
                family="Helvetica",
                size=12,
                color="#ebebeb"
            ),
            hovertemplate="Valor Promedio m2 ($MXN)<br>Trimestre=%{x}<br>Valor=%{y}<extra></extra>",
            name="Valor Promedio (m2)",
            yaxis="y1"
        ))

        fig.add_trace(go.Scatter(
            x = dff.fecha,
            y = dff.valor_mun_m2_promedio_porcentaje,
            mode="lines+markers+text",
            text = dff.valor_mun_m2_promedio_porcentaje,
            textposition = "top center",
            textfont=dict(
                family="Helvetica",
                size=14,
                color="#f78e43"
            ),
            hovertemplate="Delta V.P. m2 (%)<br>Trimestre=%{x}<br>Valor=%%{y}<extra></extra>",
            name = "Delta V.P. m2 (%)",
            yaxis = "y2"
        ))

        fig.add_trace(go.Scatter(
            x=dff.fecha,
            y=dff.valor_mun_m2_promedio,
            mode = 'lines',
            marker_color='black',
            hovertemplate="Tendencia V.P. m2 ($MXN)<br>Trimestral=%{x}<br>Valor=%{y}<extra></extra>",
            name='Tendencia V.P. m2',
            yaxis="y1"
        ))


        fig.update_layout(
            # split the x-axis to fraction of plots in
            # proportions
            xaxis=dict(
                    domain=[0.05, 0.95]
                ),
            # pass the y-axis title, titlefont, color
            # and tickfont as a dictionary and store
            # it an variable yaxis
            yaxis=dict(
                title="Valor Promedio m2 ($MXN)",
                titlefont=dict(
                    color="#0000ff"
                ),
                tickfont=dict(
                    color="#0000ff"
                )
            ),

            # pass the y-axis 2 title, titlefont, color and
            # tickfont as a dictionary and store it an
            # variable yaxis 2
            yaxis2=dict(
                title="Delta V.P. m2 (%)",
                titlefont=dict(
                    color="#FF0000"
                ),
                tickfont=dict(
                    color="#FF0000"
                ),
                anchor="free",  # specifying x - axis has to be the fixed
                overlaying="y",  # specifyinfg y - axis has to be separated
                side="right",  # specifying the side the axis should be present
                position=0.95
            ),

        )

        fig.update_layout(
            #title_text="Tendencia trimestral del valor de inmuebles en México (2019 - 2020)",
            #title_x=0.5,
            xaxis_title="Trimestre (formato: año trimestre)",
        )


        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, hovermode='x')

        fig['layout']['yaxis'].update(autorange = True)

        fig.update_layout(transition_duration=500)#, hovermode='x unified')

        return fig

@server.route("/dash")
def my_dash_app():
    return app.index()

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(host='0.0.0.0', port=port)

import sys
sys.path.append("/root/solviing_dashboard")

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from plotly import express as px
from plotly import offline as py
from plotly.graph_objs import Scatter, Layout
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from requests import options
import numpy as np
import pandas as pd

from data_process import create_df, cleanFigureData
#from . import init_app
#import package

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""

    df,options_dict = create_df()
    df_init = df[df['entidad_federativa'] == "Ciudad de México"]

    dash_app = dash.Dash(
        name='Dashboard',
        server=server,
        routes_pathname_prefix='/solviingDashboard/')
    dash_app.title = 'Solviing'
    dash_dash_appapp.layout = html.Div(id = 'parent', children = [
                    html.H1(id = 'H1', 
                            children = 'Dashboard de Vivienda en México', 
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
                                df_init['municipio'].unique(),
				'Benito Juárez',
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

    init_callbacks(dash_app, df, options_dict)

    return dash_app.server


def init_callbacks(app, df, options_dict):
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

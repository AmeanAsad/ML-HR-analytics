# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:31:58 2020

@author: amean
"""
import pandas as pd

import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import ast
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash
import appUtil
import json

PATH = "ProcessedData"
COEFFICIENTS_PATH = "{}/coefficients.json".format(PATH)
DATA_PATH = "{}/data.json".format(PATH)
NORMALIZED_DATA_PATH = "{}/normalizedData.json".format(PATH)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])


data = appUtil.getDataFrame(DATA_PATH)
normalizedData = appUtil.getDataFrame(NORMALIZED_DATA_PATH)
coefficients = appUtil.getDataFrame(COEFFICIENTS_PATH)


def dropDown(uniqueId, data, width):
    dropdown = dcc.Dropdown(
        id=uniqueId,
        options=appUtil.getLabels(data),
        value="Age",
        style={"width": width}
    )
    return dropdown


def getCorrelatorDropdowns(data):
    dropdown = dbc.Row(
        [
            dbc.Col(dropDown("correlator-1", data, "100%"), md=6),
            dbc.Col(dropDown("correlator-2", data, "100%"), md=6)
        ]
    )
    return dropdown


coefficientChart = appUtil.getCoefficientsChart(coefficients)

app.layout = html.Div(children=[
    dbc.Row(html.H1(children='Git Analysis with Python'), justify='center'),
    html.Div(id='data', style={'display': 'none'}),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='top-labels',
                              figure=coefficientChart), sm=6),
            dbc.Col([
                dbc.Row(dropDown("distplot-dropdown", data, "75%")),
                dbc.Row(dcc.Graph(id='histograms',
                                  style={"width": "100%"}))
            ], sm=6),
        ]
    ),
    #    dbc.Row([
    #            (dcc.Graph(id='histograms',
    #                       style={"width":"100%"}))
    #            ]
    #            ),
    dbc.Row(
        [
            dbc.Col([
                    getCorrelatorDropdowns(normalizedData),
                    dbc.Row(dcc.Graph(id='gauge-correlation',
                                      style={"width": "100%"}))
                    ]),
            dbc.Col([
                dbc.Row(dcc.RadioItems(
                        id='radio-items',
                        options=[
                            {'label': '   Positive   ', 'value': 'positive'},
                            {'label': '   Negative   ', 'value': 'negative'},
                        ],
                        value="positive",
                        labelStyle={"margin-right": "2%"},
                        style={"width": "100%"}
                        ),
                        style={"width": "100%"}),
                dbc.Row(dcc.Graph(id='contributers',
                                  style={"width": "100%"}))
            ], sm=6),

        ]
    )
],   style={
    'padding': "2%"
})


@app.callback(
    [Output('histograms', 'figure')],
    Input('distplot-dropdown', 'value')
)
def distPlot(value):
    chart = appUtil.getDistPlots(data, value)
    return chart


@app.callback(
    [Output('contributers', 'figure')],
    Input('radio-items', 'value')
)
def piePlot(value):
    chart = appUtil.getPieChart(coefficients, value)
    return chart


@app.callback(
    [Output('gauge-correlation', 'figure')],
    [
        Input('correlator-1', 'value'),
        Input("correlator-2", "value")
    ]
)
def correlationPlot(correlator1, correlator2):
    chart = appUtil.getCorrelationIndicator(normalizedData,
                                            correlator1,
                                            correlator2)
    return chart


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

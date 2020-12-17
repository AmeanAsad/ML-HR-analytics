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
import visdcc

text = """
Machine learning has definitely become on the biggest concepts and buzzwords in the tech industry in the past 5 years. To put some value to words, Stanford University's 2019 AI Index states that out of the organizations they have researched,  over 85%  think that Machine Learning integration will improve performance and will be required to optimize cost reduction. Indeed's job reports show that the demand for machine learning jobs in organizations has grown by 344% in 2019. The number of research papers regarding Machine Learning has more than trippled in the past two years. Safe to say, Machine learning will be a huge part of the near tech future. 

 

I started my journey learning Machine Learning a few years ago when I started engineering in University, mainly because I was interested to see what I can do with it. As a learner, I noticed you can start implementing algorithms without really understanding the underlying functionality using some existing frameworks that do most of the work for you.  It is indeed a very powerful tool, that is applicable to a lot of fields, even outside of technology and it can be used in extremely devious applications.  """


PATH = "ProcessedData"
COEFFICIENTS_PATH = "{}/coefficients.json".format(PATH)
DATA_PATH = "{}/data.json".format(PATH)
NORMALIZED_DATA_PATH = "{}/normalizedData.json".format(PATH)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
#
# commont_style = {"display": "flex",
#                 "display": "-webkit-flex",
#                 "flex-wrap": "wrap", "width": "100%", "padding": "1%", "margin-bottom": "2%"}
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


def createButtonCard():
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Navigation Menu", className="card-title"),
                    html.Div(
                        getButtonGroup()
                    ),

                ]
            ),
        ],
        style={"width": "100%", "height": "100%",
               "padding": "2%", "margin-bottom": "2%"}
    )
    return card


def getButtonGroup():
    buttonGroup = dbc.ButtonGroup(
        [
            dbc.Button("Primary", id="test", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("Primary", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("Primary", size="lg", outline=True,
                       color="dark", className="mr-1"),


        ],
        vertical=True, style={"margin-top": "10%", "width": "90%"}
    )
    return buttonGroup


def createChartCard(chart, chartid):
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Card title", className="card-title"),
                    html.Div(
                        chart
                    ),
                    dbc.Button("Go somewhere", color="primary"),
                ]
            ),
        ],
        style={"width": "100%", "padding": "1%", "margin-bottom": "2%"}
    )
    return card


def getCorrelatorDropdowns(data):
    dropdown = dbc.Row(
        [
            dbc.Col(dropDown("correlator-1", data, "100%"), md=6),
            dbc.Col(dropDown("correlator-2", data, "100%"), md=6)
        ]
    )
    return dropdown


def getCoeffChart():
    chart = dcc.Graph(id='top-labels',
                      figure=coefficientChart)
    return createChartCard(chart, "test")


def getPieChart():
    chart = html.Div([
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

    ])
    return createChartCard(chart, "test")


def getGauge():
    chart = html.Div([
        getCorrelatorDropdowns(normalizedData),
        dbc.Row(dcc.Graph(id='gauge-correlation',
                          style={"width": "100%"}))])
    return createChartCard(chart, "test")


def getDistChart():
    chart = html.Div([
        dbc.Row(dropDown("distplot-dropdown", data, "75%")),
        dbc.Row(dcc.Graph(id='histograms',
                          style={"width": "100%"}))])
    return createChartCard(chart, "test")


def getChartSection1():
    chart = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([getCoeffChart()], sm=7, xs=12),
                    dbc.Col([getPieChart()], sm=5),
                ]
            )
        ]
    )
    return chart


def getChartSection2():
    chart = dbc.Row(
        [
            dbc.Col([getDistChart()], sm=8, xs=12),
            dbc.Col([getGauge()], sm=4),
        ]
    )
    return chart

def getIntroSection():
    intro =  dbc.Row([html.H2("Short Intro"),
            html.P(text)
            ], style={"padding":"5%"})
    return intro

coefficientChart = appUtil.getCoefficientsChart(coefficients)

app.layout = html.Div(children=[
    visdcc.Run_js(id='javascript'),

    dbc.Row(html.H1(children='Git Analysis with Python'), justify='center'),
    html.Div(id='data', style={'display': 'none'}),

    dbc.Row([
        dbc.Col([html.Div([createButtonCard()],  style={"height": "100vh", "position": "sticky",
                                                        "top": "0", "zIndex": "2000", "textAlign": "center", "paddingTop": "30%",
                                                        "paddingBottom": "40%",
                                                        "background-color": "white"})], md=2),
        dbc.Col([
            getIntroSection(),
            getChartSection1(),
            getChartSection2(),

        ])


    ])


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


@app.callback(
    Output('javascript', 'run'),
    [Input('test', 'n_clicks')])
def myfun(x):
    if x:
        return """
            var elmnt = document.getElementById('gauge-correlation');
            elmnt.scrollIntoView();
                """
    return ""


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

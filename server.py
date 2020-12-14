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

import json

PATH = "ProcessedData"
COEFFICIENTS_PATH = "{}/coefficients.json".format(PATH)
DATA_PATH = "{}/data.json".format(PATH)
NORMALIZED_DATA_PATH =  "{}/normalizedData.json".format(PATH)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


def openFile(path):
    datum = {}
    with open(DATA_PATH) as dataJSON:
        loadedData = json.load(dataJSON)
        generalData = pd.DataFrame(loadedData)
    return generalData

openFile(DATA_PATH)
        
#generalData = pd.read_json(path_or_buf="ProcessingData/data.json", orient="records", lines=True)

#chart = px.bar(x=topCoefficients["features"],
#               y=topCoefficients["weights"], orientation="v")
#chart.update_layout(transition={
#    'duration': 500,
#    'easing': 'cubic-in-out'
#})
#
## print(items.head)
##classes = list(testX.columns)
##print(len(coefficients), len(classes));
#
## plt.figure()
##X = coefficients["feautres"].to_numpy()[10]
##Y = coefficients["weights"].to_numpy()[10]
## plt.show()
#
########################################################################
########################################################################
#
#
#def getLabels(df):
#    labels = list(df.columns)
#    labels = [{"value": x, "label": x} for x in labels]
#    return labels
#
#
#def getCoefficients(df, model):
#    weights = pd.DataFrame(np.transpose(model.coef_))
#
#    coefficients = pd.concat([pd.DataFrame(testX.columns),
#                              weights,
#                              abs(weights)], axis=1)
#
#    coefficients.columns = ["features", "weights", "abs_weights"]
#    coefficients = coefficients.sort_values(
#        by=["abs_weights"], ascending=False)
#    coefficients = coefficients.head(15)
#
#    return coefficients
#
#
#def getPositiveCoefficients(coefficients):
#    negativeCoefficients = coefficients[coefficients["weights"] > 0]
#    return negativeCoefficients.head(10)
#
#
#def getNegativeCoefficients(coefficients):
#    positiveCoefficients = coefficients[coefficients["weights"] < 0]
#    return positiveCoefficients.head(10)
#
#
######################################################################
######################################################################
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
#
#def dropDown():
#    dropdown = dcc.Dropdown(
#        id='time-series-dropdown',
#        options=getLabels(generalData),
#        value="Age",
#        style={"width": "100%"}
#    )
#    return dropdown
#
#
#app.layout = html.Div(children=[
#    dbc.Row(html.H1(children='Git Analysis with Python'), justify='center'),
#    html.Div(id='data', style={'display': 'none'}),
#    dbc.Row(
#        [
#            dbc.Col(dcc.Graph(id='top-labels',
#                              figure=chart),sm=6),
#            dbc.Col([
#                dbc.Row(dropDown()),
#                dbc.Row(dcc.Graph(id='histograms'))
#            ], sm=6),
#        ]
#    ),
#    dbc.Row(
#        [
#            dbc.Col(dcc.Graph(id='top-contributers',
#                              figure=chart),sm=6),
#            dbc.Col([
#                dbc.Row(dcc.RadioItems(
#                        id='radio-items',
#                        options=[
#                            {'label': '   Positive   ', 'value': 'positive'},
#                            {'label': '   Negative   ', 'value': 'negative'},
#                        ],
#                        value="positive",
#                        labelStyle= {"margin-right":"2%"},
#                        style={"width":"100%"}
#                        ), 
#                        style={"width": "100%"}),
#                dbc.Row(dcc.Graph(id='contributers'))
#            ], sm=6),
#
#        ]
#    )
#],   style={
#    'padding': "2%"
#})
#
#
#@app.callback(
#    [Output('histograms', 'figure')],
#    Input('time-series-dropdown', 'value')
#)
#def chart(value):
#    vals = generalData[value].to_numpy()
#    chart = px.histogram(x=vals)
#    chart.update_layout(transition_duration=2000,
#                        title="Number of Daily Issues")
#
#    return [chart]
#
#
#@app.callback(
#    [Output('contributers', 'figure')],
#    Input('radio-items', 'value')
#)
#def chart(value):
#    if value == "positive":
#        df = getPositiveCoefficients(coefficients)
#    else:
#        df = getNegativeCoefficients(coefficients)
#
#    chart = px.pie(df, values='abs_weights', names='features',
#                   title='Population of European continent')
#    chart.update_layout(transition_duration=2000,
#                        title="Number of Daily Issues")
#
#    return [chart]
#

#if __name__ == '__main__':
#    app.run_server(debug=True, use_reloader=False)

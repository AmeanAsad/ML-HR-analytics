# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:31:58 2020

@author: amean
"""

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash
import appUtil
import visdcc
from componentUtil import *

PATH = "ProcessedData"
COEFFICIENTS_PATH = "{}/coefficients.json".format(PATH)
DATA_PATH = "{}/data.json".format(PATH)
NORMALIZED_DATA_PATH = "{}/normalizedData.json".format(PATH)
TEXT_PATH = "text.json"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server
app.title = "Unessay"
devMode = False
data = appUtil.getDataFrame(DATA_PATH)
normalizedData = appUtil.getDataFrame(NORMALIZED_DATA_PATH)
coefficients = appUtil.getDataFrame(COEFFICIENTS_PATH)
text = appUtil.getTextObject(TEXT_PATH)


app.layout = html.Div(children=[
    visdcc.Run_js(id='intro1'),
    visdcc.Run_js(id='mon1'),
    visdcc.Run_js(id='dat1'),
    visdcc.Run_js(id='mod1'),
    visdcc.Run_js(id='viz1'),
    visdcc.Run_js(id='gd1'),
    visdcc.Run_js(id='bd1'),
    visdcc.Run_js(id='cnc1'),

    dbc.Row([
        dbc.Col([html.Div([])], md=4),
        dbc.Col(dbc.Row(
            html.H1(children='Machine Learning in Organizations'),
            justify="center"), md=4),
        dbc.Col(getHeader(), align="right")
    ]),
    html.Div(id='data', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([html.Div([createButtonCard()],
                          style={"height": "100vh", "position": "sticky",
                                 "top": "0", "zIndex": "2000", "textAlign": "center", "paddingTop": "30%",
                                 "paddingBottom": "40%",

                                 "background-color": "white"})], lg=2),
        dbc.Col([
            createSection("shortIntro", "Short Intro", "introduction"),
            createSection("longIntro", "The Monologue", "monologue"),
            createSection("data", "About the Data", "about-data"),
            createSection("model", "The Machine Learning Model", "model"),
            createSection("dashboard", "Visualization Dashboard", "dashboard"),
            getChartSection1(),
            getChartSection2(),
            createSection("good", "The Good Side", "good"),
            createSection("bad", "The Dark Side", "bad"),
            createSection("conclusion", "A Final Note", "conc"),


        ])


    ])


],   style={
    'padding': "2%"
})


def modalOpen(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


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
    Output("modalmd1", "is_open"),
    [Input("openmd1", "n_clicks"), Input("closemd1", "n_clicks")],
    [State("modalmd1", "is_open")],
)
def toggle_modal1(n1, n2, is_open):
    return modalOpen(n1, n2, is_open)


@app.callback(
    Output("modalmd2", "is_open"),
    [Input("openmd2", "n_clicks"), Input("closemd2", "n_clicks")],
    [State("modalmd2", "is_open")],
)
def toggle_modal2(n1, n2, is_open):
    return modalOpen(n1, n2, is_open)


@app.callback(
    Output("modalmd3", "is_open"),
    [Input("openmd3", "n_clicks"), Input("closemd3", "n_clicks")],
    [State("modalmd3", "is_open")],
)
def toggle_modal3(n1, n2, is_open):
    return modalOpen(n1, n2, is_open)


@app.callback(
    Output("modalmd4", "is_open"),
    [Input("openmd4", "n_clicks"), Input("closemd4", "n_clicks")],
    [State("modalmd4", "is_open")],
)
def toggle_modal4(n1, n2, is_open):
    return modalOpen(n1, n2, is_open)


@app.callback(
    Output('intro1', 'run'),
    [Input('intro', 'n_clicks')])
def myfun1(x):
    if x:
        return """
            var elmnt = document.getElementById('introduction');
            elmnt.scrollIntoView();
                """
    return ""


@app.callback(
    Output('mon1', 'run'),
    [Input('mon', 'n_clicks')])
def myfun2(x):
    if x:
        return """
            var elmnt = document.getElementById('monologue');
            elmnt.scrollIntoView();
                """
    return ""


@app.callback(
    Output('dat1', 'run'),
    [Input('dat', 'n_clicks')])
def myfun3(x):
    if x:
        return """
            var elmnt = document.getElementById('about-data');
            elmnt.scrollIntoView();
                """
    return ""


@app.callback(
    Output('mod1', 'run'),
    [Input('mod', 'n_clicks')])
def myfun4(x):
    if x:
        return """
            var elmnt = document.getElementById('model');
            elmnt.scrollIntoView();
                """
    return ""


@app.callback(
    Output('viz1', 'run'),
    [Input('viz', 'n_clicks')])
def myfun5(x):
    if x:
        return """
            var elmnt = document.getElementById('dashboard');
            elmnt.scrollIntoView();
                """
    return ""


@app.callback(
    Output('gd1', 'run'),
    [Input('gd', 'n_clicks')])
def myfun6(x):
    if x:
        return """
            var elmnt = document.getElementById('good');
            elmnt.scrollIntoView();
                """
    return ""


@app.callback(
    Output('bd1', 'run'),
    [Input('bd', 'n_clicks')])
def myfun7(x):
    if x:
        return """
            var elmnt = document.getElementById('bad');
            elmnt.scrollIntoView();
                """
    return ""


@app.callback(
    Output('cnc1', 'run'),
    [Input('cnc', 'n_clicks')])
def myfun8(x):
    if x:
        return """
            var elmnt = document.getElementById('conc');
            elmnt.scrollIntoView();
                """
    return ""


if __name__ == '__main__':
    app.run_server(debug=devMode, use_reloader=False)

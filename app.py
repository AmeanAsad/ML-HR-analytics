# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:31:58 2020

@author: amean
"""

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash
import appUtil
import visdcc

PATH = "ProcessedData"
COEFFICIENTS_PATH = "{}/coefficients.json".format(PATH)
DATA_PATH = "{}/data.json".format(PATH)
NORMALIZED_DATA_PATH = "{}/normalizedData.json".format(PATH)
TEXT_PATH = "text.json"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server
data = appUtil.getDataFrame(DATA_PATH)
normalizedData = appUtil.getDataFrame(NORMALIZED_DATA_PATH)
coefficients = appUtil.getDataFrame(COEFFICIENTS_PATH)
text = appUtil.getTextObject(TEXT_PATH)


def dropDown(uniqueId, data, width):
    dropdown = dcc.Dropdown(
        id=uniqueId,
        options=appUtil.getLabels(data),
        value="Age",
        style={"width": width}
    )
    return dropdown


def createSection(textObject, title, sectionId):
    textList = text[textObject]
    paragraphs = [html.P([item]) for item in textList]
    section = dbc.Row([html.H2(title, id=sectionId),
                       html.Div(paragraphs),
                       ], style={"paddingTop": "2%", "paddingLeft": "3%", "paddingRight": "3%"})
    return section


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
            dbc.Button("Short Intro", id="intro", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("The Monologue", id="mon", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("About the Data", id="dat", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("The ML Model", id="mod", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("Visualization Dashboard", id="viz", size="lg",
                       outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("The Good Side", id="good", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("The Dark Side", id="bad", size="lg", outline=True,
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
                    dbc.Col([getCoeffChart()], lg=7),
                    dbc.Col([getPieChart()], lg=5),
                ]
            )
        ]
    )
    return chart


def getChartSection2():
    chart = dbc.Row(
        [
            dbc.Col([getDistChart()], lg=8),
            dbc.Col([getGauge()], lg=4),
        ]
    )
    return chart


coefficientChart = appUtil.getCoefficientsChart(coefficients)

app.layout = html.Div(children=[
    visdcc.Run_js(id='intro1'),
    visdcc.Run_js(id='mon1'),
    visdcc.Run_js(id='dat1'),
    visdcc.Run_js(id='mod1'),
    visdcc.Run_js(id='viz1'),

    dbc.Row(html.H1(children='Machine Learning in Organizations'), justify='center'),
    html.Div(id='data', style={'display': 'none'}),

    dbc.Row([
        dbc.Col([html.Div([createButtonCard()],  style={"height": "100vh", "position": "sticky",
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


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

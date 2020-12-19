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


def dropDown(uniqueId, data, width, val):
    dropdown = dcc.Dropdown(
        id=uniqueId,
        options=appUtil.getLabels(data),
        value=val,
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


def createModalSection(textObject):
    textList = text[textObject]
    paragraphs = [html.P([item]) for item in textList]
    section = html.Div(paragraphs),
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


def getModal(name):
    modal = html.Div(
        [
            dbc.Button("Figure Information", id="open" + name),
            dbc.Modal(
                [
                    dbc.ModalBody(createModalSection(name)),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close" +
                                   name, className="ml-auto")
                    ),
                ],
                id="modal"+name,
            ),
        ]
    )
    return modal


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
            dbc.Button("The Good Side", id="gd", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("The Dark Side", id="bd", size="lg", outline=True,
                       color="dark", className="mr-1"),
            dbc.Button("Final Note", id="cnc", size="lg", outline=True,
                       color="dark", className="mr-1"),


        ],
        vertical=True, style={"margin-top": "10%", "width": "90%"}
    )
    return buttonGroup


def createChartCard(chart, title, modalName):
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    html.Div(
                        chart
                    ),
                    getModal(modalName),
                ]
            ),
        ],
        style={"width": "100%", "padding": "1%", "margin-bottom": "2%"}
    )
    return card


def getCorrelatorDropdowns(data):
    dropdown = dbc.Row(
        [
            dbc.Col(dropDown("correlator-1", data, "100%", "Turnover"), md=6),
            dbc.Col(dropDown("correlator-2", data,
                             "100%", "YearsWithCurrManager"), md=6)
        ]
    )
    return dropdown


def getCoeffChart():
    chart = dcc.Graph(id='top-labels',
                      figure=coefficientChart)
    return createChartCard(chart, "Figure 1: Feature Importance", "md1")


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
    return createChartCard(chart, "Figure 4: Contributing Features", "md4")


def getGauge():
    chart = html.Div([
        getCorrelatorDropdowns(normalizedData),
        dbc.Row(dcc.Graph(id='gauge-correlation',
                          style={"width": "100%"}))])
    return createChartCard(chart, "Figure 2: Correlations", "md2")


def getDistChart():
    chart = html.Div([
        dbc.Row(dropDown("distplot-dropdown", data, "75%", "Age")),
        dbc.Row(dcc.Graph(id='histograms',
                          style={"width": "100%"}))])
    return createChartCard(chart, "Figure 3: Dsitribution Plots", "md3")


def getChartSection1():
    chart = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([getCoeffChart()], lg=8),
                    dbc.Col([getGauge()], lg=4),

                ]
            )
        ]
    )
    return chart


def getChartSection2():
    chart = dbc.Row(
        [
            dbc.Col([getDistChart()], lg=7),
            dbc.Col([getPieChart()], lg=5),
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
    visdcc.Run_js(id='gd1'),
    visdcc.Run_js(id='bd1'),
    visdcc.Run_js(id='cnc1'),

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
    app.run_server(debug=True, use_reloader=False)

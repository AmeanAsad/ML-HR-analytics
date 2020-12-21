# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:25:53 2020

@author: amean
"""
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import json
import appUtil


PATH = "ProcessedData"
COEFFICIENTS_PATH = "{}/coefficients.json".format(PATH)
DATA_PATH = "{}/data.json".format(PATH)
NORMALIZED_DATA_PATH = "{}/normalizedData.json".format(PATH)
TEXT_PATH = "text.json"

data = appUtil.getDataFrame(DATA_PATH)
normalizedData = appUtil.getDataFrame(NORMALIZED_DATA_PATH)
coefficients = appUtil.getDataFrame(COEFFICIENTS_PATH)
text = appUtil.getTextObject(TEXT_PATH)
TEXT_PATH = "text.json"


coefficientChart = appUtil.getCoefficientsChart(coefficients)


def getTextObject(path):
    with open(path) as dataJSON:
        data = json.load(dataJSON)
    return data


text = getTextObject(TEXT_PATH)


def getHeader():
    return dbc.Row([
        dbc.Button("By Amean Asad", color="dark", href="https://ameanasad.tech/",size="lg", style={
                "marginRight":"3%"}),
        dbc.Button("Project Github", color="dark",size="lg", href="https://github.com/AmeanAsad/ML-HR-analytics"),

    ], justify="center")


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

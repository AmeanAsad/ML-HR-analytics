# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:54:51 2020

@author: amean
"""

import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
TEMPLATE = "plotly"
px.defaults.color_continuous_scale = px.colors.sequential.RdBu

def getTextObject(path):
    with open(path) as dataJSON:
        data = json.load(dataJSON)
    return data

    
def getDataFrame(path):
    with open(path) as dataJSON:
        loadedData = json.load(dataJSON)
        dataframe = pd.DataFrame(loadedData)
    return dataframe


def getDistPlots(data, value):
    vals = data[value].to_numpy()
    chart = px.histogram(data, x=value,
                         color_discrete_sequence=['#1f77b4', ],
                         template=TEMPLATE)
    chart.update_layout(transition_duration=2000,
                        autosize=True,
                        bargap=0.2,

                        title="Number of Daily Issues")
#    chart.update_traces(marker_color='#1f77b4' , marker_line_color='#1f77b4',
#                  marker_line_width=2.5)
    return [chart]


def getCorrelationIndicator(data, value1, value2):
    correlation = data[value1].corr(data[value2])

    figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=correlation,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'visible': False, 'range': [-1, 1]},
            'bar': {'color': "black", "thickness": 0.2},

            'steps': [
                {'range': [-1, 0], 'color': "#F08080"},
                {'range': [0, 1], 'color': "#90EE90"}],
        },
        title={'text': "Variable Correlation"}))
    figure.update_layout(transition_duration=2000,
                         title="Number of Daily Issues")
    return [figure]


def getPieChart(coefficients, value):
    colors = ["#03045e", "#023e8a", "#0077b6", "#0096c7",
              "#00b4d8", "#48cae4", "#90e0ef", "#ade8f4", "#caf0f8", "#F0F8FF"]
    if value == "positive":
        df = getPositiveCoefficients(coefficients)
        chart = px.pie(df, values='abs_weights', names='features',
                       template=TEMPLATE,
                       hole=0.4,
                       color_discrete_sequence=colors,
                       height=500,
                       title='Factors Contributing to Attrition')
    else:
        df = getNegativeCoefficients(coefficients)
        chart = px.pie(df, values='abs_weights', names='features',
                       template=TEMPLATE,
                       color_discrete_sequence=colors,
                       hole= 0.4,
                       height=500,
                       title='Factors Keeping Employees Stay')

    chart.update_layout(transition_duration=2000,
                        autosize=True
                        )
    chart.update_traces(marker=dict( line=dict(color='#495057', width=0.7)))
    return [chart]


def getCoefficientsChart(coefficients):
    topCoefficients = coefficients.head(20)
    chart = px.bar(topCoefficients, x="features",
                   y="weights",
                   color="weights",
                   height=520,
                   orientation="v",
                   #                   height=500,
                   template=TEMPLATE)
    chart.update_layout(bargap=0.2,
                        title="Number of Daily Issues",
                        autosize=True,
                        transition={
                            'duration': 500,
                            'easing': 'cubic-in-out'
                        })
    chart.update_traces(marker_line_color='#495057',
                  marker_line_width=1)
    return chart


def getLabels(df):
    labels = list(df.columns)
    labels = [{"value": x, "label": x} for x in labels]
    return labels


def getCoefficients(df, model):
    weights = pd.DataFrame(np.transpose(model.coef_))

    coefficients = pd.concat([pd.DataFrame(df.columns),
                              weights,
                              abs(weights)], axis=1)
    
    coefficients.columns = ["features", "weights", "abs_weights"]
    coefficients = coefficients.sort_values(
        by=["abs_weights"], ascending=False)
    coefficients = coefficients.head(15)

    return coefficients


def getPositiveCoefficients(coefficients):
    negativeCoefficients = coefficients[coefficients["weights"] > 0]
    return negativeCoefficients.head(10)


def getNegativeCoefficients(coefficients):
    positiveCoefficients = coefficients[coefficients["weights"] < 0]
    return positiveCoefficients.head(10)

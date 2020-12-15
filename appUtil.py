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

TEMPLATE = "simple_white"


def getDataFrame(path):
    with open(path) as dataJSON:
        loadedData = json.load(dataJSON)
        dataframe = pd.DataFrame(loadedData)
    return dataframe


def getDistPlots(data, value):
    vals = data[value].to_numpy()
    chart = px.histogram(data, x=value, template=TEMPLATE)
    chart.update_layout(transition_duration=2000,
                        autosize=True,
                        title="Number of Daily Issues")
    return [chart]


def getCorrelationIndicator(data, value1, value2):
    correlation = data[value1].corr(data[value2])

    figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=correlation,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Variable Correlation"}))
    return [figure]


def getPieChart(coefficients, value):
    if value == "positive":
        df = getPositiveCoefficients(coefficients)
        chart = px.pie(df, values='abs_weights', names='features',
                       template=TEMPLATE,
                       title='Factors Contributing to Attrition')
    else:
        df = getNegativeCoefficients(coefficients)
        chart = px.pie(df, values='abs_weights', names='features',
                       template=TEMPLATE,
                       title='Factors Keeping Employees Stay')

    chart.update_layout(transition_duration=2000,
                        autosize=True)
    return [chart]


def getCoefficientsChart(coefficients):
    topCoefficients = coefficients.head(15)
    chart = px.bar(x=topCoefficients["features"],
                   y=topCoefficients["weights"],
                   orientation="v",
                   height=700,
                   template=TEMPLATE)
    chart.update_layout(transition={
        'duration': 500,
        'easing': 'cubic-in-out'
    })
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

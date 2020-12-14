# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:54:51 2020

@author: amean
"""

import pandas as pd
import json
import plotly.express as px
import numpy as np


def getDataFrame(path):
    with open(path) as dataJSON:
        loadedData = json.load(dataJSON)
        dataframe = pd.DataFrame(loadedData)
    return dataframe


def getDistPlots(data, value):
    vals = data[value].to_numpy()
    chart = px.histogram(x=vals)
    chart.update_layout(transition_duration=2000,
                        title="Number of Daily Issues")
    return [chart]


def getPieChart(coefficients, value):
    if value == "positive":
        df = getPositiveCoefficients(coefficients)
        chart = px.pie(df, values='abs_weights', names='features',
                       title='Factors Contributing to Attrition')
    else:
        df = getNegativeCoefficients(coefficients)
        chart = px.pie(df, values='abs_weights', names='features',
                       title='Factors Keeping Employees Stay')

    chart.update_layout(transition_duration=2000)
    return [chart]


def getCoefficientsChart(coefficients):
    topCoefficients = coefficients.head(15)
    chart = px.bar(x=topCoefficients["features"],
                   y=topCoefficients["weights"], orientation="v")
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

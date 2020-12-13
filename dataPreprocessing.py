#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import ast
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash
"""
Created on Sat Nov 21 20:40:13 2020

@author: ameanasad
"""


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import train_test_split


dataLocation = "EmployeeData"

# Prepare file directories for each data surveyed
generalDataLocation = dataLocation + "/general_data.csv"
employeeSurveyLocation = dataLocation + "/employee_survey_data.csv"
managerSurveyLocation = dataLocation + "/manager_survey_data.csv"

generalData = pd.read_csv(generalDataLocation)
generalData.sort_values(by=['EmployeeID'])
turnover = generalData["Attrition"]
generalData = generalData.drop(
    columns=["Attrition", "Over18", "EmployeeCount", "StandardHours"])

managerSurveyData = pd.read_csv(managerSurveyLocation)
employeeSurveyData = pd.read_csv(employeeSurveyLocation)

managerSurveyData = managerSurveyData.sort_values(by=["EmployeeID"])
employeeSurveyData = employeeSurveyData.sort_values(by=["EmployeeID"])

managerSurveyData = managerSurveyData.drop(columns=["EmployeeID"])
employeeSurveyData = employeeSurveyData.drop(columns=["EmployeeID"])

generalData = generalData.join([managerSurveyData, employeeSurveyData])
generalData = generalData.drop(columns=["EmployeeID"])

categoricalData = list(generalData.select_dtypes(include='object').columns)

# 1 -> Employee left
# 0 -> Employee remains
turnover = pd.DataFrame(
    np.where(turnover == "Yes", 1, 0), columns=["Turnover"])


def encodeStringCategories(columns, df):
    """
    Parameters
    ----------
    columns : List
        List of string columns to encode.
    df : Pandas Dataframe
        Dataframe containing the feature data.

    Returns
    -------
    df : Pandas Dataframe
        Dataframe containing feature data with all the categorical data being
        one-hot encoded.
    """
    for column in columns:
        oneHotEncoding = pd.get_dummies(df[column])
        df = df.drop(columns=[column])
        df = df.join(oneHotEncoding, rsuffix="test")
    return df


data = encodeStringCategories(categoricalData, generalData)
data = data.join(turnover)
data = data.drop(columns=["Human Resourcestest"])
# Remove any null valued data
data = data.fillna(0)
# Data Normalization
data = ((data-data.min())/(data.max() - data.min()))


train, test = train_test_split(data, test_size=0.25)

trainY = train["Turnover"]
trainX = train.drop(columns=["Turnover"])
testY = test["Turnover"]
testY = testY.to_numpy(dtype=int)
testX = test.drop(columns=["Turnover"])

regressor = LogisticRegression(
    solver="saga", max_iter=150, penalty="elasticnet", l1_ratio=0.2)
regressor.fit(trainX, trainY)

score = regressor.score(testX, testY)
print(score)
predictions = regressor.predict(testX)


weights = pd.DataFrame(np.transpose(regressor.coef_))

coefficients = pd.concat([pd.DataFrame(testX.columns),
                          weights,
                          abs(weights)], axis=1)


coefficients.columns = ["features", "weights", "abs_weights"]
coefficients = coefficients.sort_values(by=["abs_weights"], ascending=False)

negativeCoefficients = coefficients[coefficients["weights"] < 0]
positiveCoefficients = coefficients[coefficients["weights"] > 0]

topCoefficients = coefficients.head(15)


cm = metrics.confusion_matrix(testY, predictions)

chart = px.bar(x=topCoefficients["features"],
               y=topCoefficients["weights"], orientation="v")
chart.update_layout(transition={
    'duration': 500,
    'easing': 'cubic-in-out'
})

# print(items.head)
#classes = list(testX.columns)
#print(len(coefficients), len(classes));

# plt.figure()
#X = coefficients["feautres"].to_numpy()[10]
#Y = coefficients["weights"].to_numpy()[10]
# plt.show()

#######################################################################
#######################################################################


def getLabels(df):
    labels = list(df.columns)
    labels = [{"value": x, "label": x} for x in labels]
    return labels


def getCoefficients(df, model):
    weights = pd.DataFrame(np.transpose(model.coef_))

    coefficients = pd.concat([pd.DataFrame(testX.columns),
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


#####################################################################
#####################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def dropDown():
    dropdown = dcc.Dropdown(
        id='time-series-dropdown',
        options=getLabels(generalData),
        value="Age",
        style={"width": "100%"}
    )
    return dropdown


app.layout = html.Div(children=[
    dbc.Row(html.H1(children='Git Analysis with Python'), justify='center'),
    html.Div(id='data', style={'display': 'none'}),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='top-labels',
                              figure=chart),sm=6),
            dbc.Col([
                dbc.Row(dropDown()),
                dbc.Row(dcc.Graph(id='histograms'))
            ], sm=6),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='top-contributers',
                              figure=chart),sm=6),
            dbc.Col([
                dbc.Row(dcc.RadioItems(
                        id='radio-items',
                        options=[
                            {'label': '   Positive   ', 'value': 'positive'},
                            {'label': '   Negative   ', 'value': 'negative'},
                        ],
                        value="positive",
                        labelStyle= {"margin-right":"2%"},
                        style={"width":"100%"}
                        ), 
                        style={"width": "100%"}),
                dbc.Row(dcc.Graph(id='contributers'))
            ], sm=6),

        ]
    )
],   style={
    'padding': "2%"
})


@app.callback(
    [Output('histograms', 'figure')],
    Input('time-series-dropdown', 'value')
)
def chart(value):
    vals = generalData[value].to_numpy()
    chart = px.histogram(x=vals)
    chart.update_layout(transition_duration=2000,
                        title="Number of Daily Issues")

    return [chart]


@app.callback(
    [Output('contributers', 'figure')],
    Input('radio-items', 'value')
)
def chart(value):
    if value == "positive":
        df = getPositiveCoefficients(coefficients)
    else:
        df = getNegativeCoefficients(coefficients)

    chart = px.pie(df, values='abs_weights', names='features',
                   title='Population of European continent')
    chart.update_layout(transition_duration=2000,
                        title="Number of Daily Issues")

    return [chart]


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

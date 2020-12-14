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
    columns=["Over18", "EmployeeCount", "StandardHours"])

generalData.to_json(path_or_buf = "ProcessedData/data.json", orient="records" )

generalData = generalData.drop(columns=["Attrition"])
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

data.to_json(path_or_buf="ProcessedData/normalizedData.json")

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
coefficients.to_json(path_or_buf="ProcessedData/coefficients.json")

topCoefficients = coefficients.head(15)

cm = metrics.confusion_matrix(testY, predictions)


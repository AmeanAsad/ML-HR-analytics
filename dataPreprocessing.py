#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:40:13 2020

@author: ameanasad
"""


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split


dataLocation = "EmployeeData"

# Prepare file directories for each data surveyed
generalDataLocation = dataLocation + "/general_data.csv"
employeeSurveyLocation = dataLocation + "/employee_survey_data.csv"
managerSurveyLocation = dataLocation + "/manager_survey_data.csv"

generalData = pd.read_csv(generalDataLocation);
generalData.sort_values(by=['EmployeeID'])
turnover = generalData["Attrition"]
generalData = generalData.drop(columns=["Attrition", "Over18", "EmployeeCount", "StandardHours"])

managerSurveyData = pd.read_csv(managerSurveyLocation);
employeeSurveyData = pd.read_csv(employeeSurveyLocation);

managerSurveyData = managerSurveyData.sort_values(by=["EmployeeID"])
employeeSurveyData = employeeSurveyData.sort_values(by=["EmployeeID"])

managerSurveyData = managerSurveyData.drop(columns=["EmployeeID"])
employeeSurveyData = employeeSurveyData.drop(columns=["EmployeeID"])

generalData = generalData.join([managerSurveyData, employeeSurveyData])
generalData = generalData.drop(columns=["EmployeeID"])

categoricalData =  list(generalData.select_dtypes(include='object').columns)

# 1 -> Employee left
# 0 -> Employee remains
turnover = pd.DataFrame(np.where(turnover == "Yes", 1, 0), columns=["Turnover"])


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
        df = df.drop(columns = [column])
        df = df.join(oneHotEncoding, rsuffix="test")
    return df


data = encodeStringCategories(categoricalData, generalData)
data = data.join(turnover)

# Remove any null valued data
data = data.fillna(0);

# Data Normalization
data = ((data-data.min())/(data.max() - data.min()))


train, test = train_test_split(data, test_size=0.25)

trainY = train["Turnover"]
trainX = train.drop(columns=["Turnover"])

testY = test["Turnover"]
testY = testY.to_numpy(dtype=int);
testX = test.drop(columns=["Turnover"])



regressor = LogisticRegression(solver="saga", max_iter=150, penalty="elasticnet", l1_ratio=0.2)


regressor.fit(trainX, trainY)

print(regressor.score(testX, testY))
predictions = regressor.predict(testX)


count = 0
for i in range(len(predictions)):
    if (predictions[i] == testY[i]):
        count+=1
    

#print(count/len(testY))
        
#svm = SVC(random_state=1, gamma='auto')
#svm.fit(trainX, trainY)
#svm_prediction = svm.predict(testX)
#svm_score = svm.score(testX, testY)
#print(svm_score)
#
#    



coefficients = regressor.coef_[0]
classes = list(testX.columns)
print(len(coefficients), len(classes));

plt.figure()
plt.barh(classes, coefficients)
plt.show()














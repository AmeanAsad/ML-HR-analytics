#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:40:13 2020

@author: ameanasad
"""


import pandas as pd

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



def encodeStringCategories(columns, df):
    """
    Parameters
    ----------
    columns : TYPE
        DESCRIPTION.
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.
    """
    for column in columns:
        oneHotEncoding = pd.get_dummies(df[column])
        df = df.drop(columns = [column])
        df = df.join(oneHotEncoding, rsuffix="test")
    return df


data = encodeStringCategories(categoricalData, generalData)
data = data.fillna(0);
data = ((data-data.min())/(data.max()-data.min()))

























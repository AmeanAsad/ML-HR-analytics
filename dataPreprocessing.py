#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:40:13 2020

@author: ameanasad
"""


import pandas as pd
import ast



dataLocation = "EmployeeData"

generalDataLocation = dataLocation + "/general_data.csv"
employeeSurveyLocation = dataLocation + "/employee_survey_data.csv"
managerSurveyLocation = dataLocation + "/manager_survey_data.csv"

generalData = pd.read_csv(generalDataLocation, converters={"Age": ast.literal_eval});


test = generalData["Age"].unique
print(test)


























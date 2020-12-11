#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:27:31 2020

@author: ameanasad
"""


import pandas as pd
import ast
# import plotly.graph_objs as go
# from plotly.offline import plot
from datetime import datetime as dt



df = pd.read_csv("dap-planning.csv", converters={"label": ast.literal_eval,
                                                 "assignees": ast.literal_eval})

# df.created_at.apply(lambda date: dt.strptime(date,  "%Y-%m-%dT%H:%M:%SZ"))

# df_label = df.explode('label')

# test = pd.DataFrame(df_label.groupby(['label','type'])['type'].count().unstack())
# print(test.first())

# label_count = df_label.groupby("label")['label'].count().reset_index(name="count")
# label_count = label_count.sort_values(by=['count'], ascending=False)

# g = go.Bar(x=label_count['label'].to_numpy()[:10], y=label_count['count'].to_numpy()[:10])
# data = [g]

# fig = dict(data=data)
# plot(fig)




def getTop10Labels(df):
    df_label = df.explode('label')
    label_count = df_label.groupby("label")['label'].count().reset_index(name="count")
    label_count = label_count.sort_values(by=['count'], ascending=False)
    return label_count
    
def getAssigneeList(df):
    assignee_list = []
    assignee_df =  df.explode("assignees")
    for assignee in assignee_df.assignees.unique():
        assignee_object = {
            "label": str(assignee),
            "value": str(assignee),
            }
        assignee_list.append(assignee_object)
    return assignee_list
def getLabelsList(df):
    labels = []
    labels_df = df.explode("label")
    for label in labels_df.label.unique():
        label_object = {
                "label": str(label),
                "value": str(label)
            }
        labels.append(label_object)
    return labels

def getAssigneeIssues(df, name):
    df = df.explode("assignees")
    df = df[df['assignees'].str.contains(name, na=False)]
    return df

def getIssuesByRelatedLabel(df, selection):
     df['val'] = df['label'].apply(lambda x: str("".join(x)))
     df['val'] = df['label'].apply(lambda x: all(y in str(x) for y in selection))
     df = df[df['val'] == True]
     return df
    
def indexByDateRange(df, start, end=dt.strftime(dt.now(),'%Y-%m-%d')):
    # start = dt.strptime(start,'%Y-%m-%d')
    # end = dt.strptime(end, '%Y-%m-%d')
    # df.created_at.apply(lambda date: dt.strptime(date,  "%Y-%m-%dT%H:%M:%SZ"))
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] =  df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d')).astype(str)
    df['date'] = df['created_at']
    df = df.set_index('created_at')
    df = df.sort_index()
    return df.loc[start: end]

def numofIssuesByDate(df):
    openIssues = df[df['status']=="open"]
    closedIssues = df[df['status']=="closed"]
    groupOpen = openIssues.groupby("date")['url'].count().reset_index(name="open")
    groupClosed = closedIssues.groupby("date")['url'].count().reset_index(name="closed")
    groupObject = {"open" : [groupOpen['date'].to_list(), groupOpen['open'].to_list()],
                   "closed" : [groupClosed['date'].to_list(), groupClosed['closed'].to_list()]}
    return groupObject

def pieTop10Labels(df):
    df_label = df.explode('label')
    label_count = df_label.groupby("label")['label'].count().reset_index(name="count")
    label_count = label_count.sort_values(by=['count'], ascending=False)
    return label_count[:10]
    
def getIssuesStacked(df):
    stack_layers = []
    
    # df = indexByDateRange(df, "2020-01-12", "2020-08-23")
    df = df.explode("label")
    df = df.groupby(["label","status"])['url'].count().reset_index(name="count")
    df = df.pivot(index="status", columns="label", values="count")
    df = df.sort_values(by=['open'],axis=1, ascending=False)
    df = df[df.columns[:10]]
    for column in df.columns:
        stack_layer =  {
            "name": str(column),
            "data" : [df[column]['open'], df[column]['closed']],
            "labels" : ['open', 'closed'],
            "color": None     
        }
        stack_layers.append(stack_layer)
        
    return stack_layers

def getOpenClosedIssueCount(df):
    df = df.groupby("status")['url'].count().reset_index(name="count")
    return df


# df.created_at.apply(lambda date: dt.strptime(date,  "%Y-%m-%dT%H:%M:%SZ"))
# df['created_at'] = pd.to_datetime(df['created_at'])
# df.created_at.apply(lambda x: x.strftime('%Y-%m-%d')).astype(str)
# df = df.set_index('created_at')

# df = df.sort_index()
# df = indexByDateRange(df, start, end)

# in_range_df = df[df["created_at"].isin(pd.date_range("2016-01-15", "2020-01-20"))]
test = indexByDateRange(df, "2020-06-12", "2020-08-23")
test = numofIssuesByDate(test)
# df = test.explode("label")
# df = df.groupby(["label","status"])['url'].count().reset_index(name="count")
# df = df.pivot(index="status", columns="label", values="count")
# df = df.sort_values(by=['closed'],axis=1, ascending=False)
# test = df[df.columns[:10]]

# selection = ["CP4D", "type:defect"]
# test = test.groupby(['date', 'status'])['status'].value_counts()
# test = pd.DataFrame(test.label.tolist())

# test['val'] = test['label'].apply(lambda x: str("".join(x)))
# test['val'] = test['label'].apply(lambda x: all(y in str(x) for y in selection))
# test = test[test['val']==True]
# test = test.explode("assignees")
# test = test[test['assignees'].str.contains('Richard', na=False)]


# test = test.explode("label")
# test = pieTop10Labels(df)
# print(test['count'].to_numpy())

df['time'] = df['time'].apply(lambda x: x[:-3])

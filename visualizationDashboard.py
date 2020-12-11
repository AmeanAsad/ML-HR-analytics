#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 21:08:55 2020

@author: ameanasad
"""


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import ast
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import gitAnalysis
from datetime import datetime as dt

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

#
#datum = pd.read_csv("dap-planning.csv", converters={"label": ast.literal_eval,
#                                                 "assignees": ast.literal_eval})
# df_label = df.explode('label')
# label_count = df_label.groupby("label")['label'].count().reset_index(name="count")
# label_count = label_count.sort_values(by=['count'], ascending=False)
# fig = px.bar(df, x=label_count['label'].to_numpy()[:10], y=label_count['count'].to_numpy()[:10])

# num_issues_by_date = gitAnalysis.numofIssuesByDate(df, "2020-04-01", "2020-08-24")

# fig2 = px.line(x=num_issues_by_date[0], y=num_issues_by_date[1])


def dateInputs():
    today = dt.today()
    inputs = dbc.Row(
       [
        dcc.DatePickerRange(
           id='my-date-picker-range',
           end_date=dt.now(),
           display_format='YYYY-MM-DD',
           start_date_placeholder_text='Start',
           start_date=dt(today.year, 1, 1),
           min_date_allowed="2016-08-31",
           max_date_allowed=dt.now(),
           style={"color":"blue"}
           
           )  
        ], justify='center' )
    return inputs

    
app.layout = html.Div(children=[
    dbc.Row( html.H1(children='Git Analysis with Python'), justify='center'),
    dateInputs(),
    html.Div(id='data', style={'display': 'none'}),
    dbc.Row(
        [     
            dbc.Col(
                [ dbc.Row(
                        dcc.Dropdown(
                                id='time-series-dropdown',
                                options=gitAnalysis.getLabelsList(datum),
                                value=["CP4D"],
                                multi=True,
                                style={"width": "100%"}
                        ), style={"width": "100%"}),
                    dbc.Row(dcc.Graph(id='issue-time-series'))
                ], width=6),
            dbc.Col(dcc.Graph(id='bar-plot'), width=6)   
        ]
        ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='pie-chart')),
            dbc.Col(dcc.Graph(id='top-labels'),),
        ]
        ),
    dbc.Row(
        dbc.Col(dcc.Dropdown(
        id='dropdown',
        placeholder="Select Team Member",
        value="Richard-Tang"
        # style={"width": "40%"}
        ), width=4), justify='center'),
    
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='pie-chart2')),
            dbc.Col(dcc.Graph(id='top-labels2'),),
        ]
        ),
    ],   style={
            'padding':"2%"
    }) 
        
        
        

@app.callback([Output('data', 'children')
                ],
               [Input('my-date-picker-range', 'start_date'),
                Input('my-date-picker-range', 'end_date'),
                ]
              )
def getDates(start_date, end_date):
    df = gitAnalysis.indexByDateRange(datum, start_date, end_date)
    df.reset_index(inplace=True)

    return [df.to_json()]



@app.callback(
         [Output('issue-time-series', 'figure'),
          ],
          [  
          Input('data', 'children'),
          Input('time-series-dropdown', 'value')
          ]
    )
def timeSeries(jsonified_cleaned_data, value):
    data = pd.read_json(jsonified_cleaned_data)
    relatedLabels = gitAnalysis.getIssuesByRelatedLabel(data, value)
    num_issues_by_date = gitAnalysis.numofIssuesByDate(relatedLabels)

    
    
    openIssues = num_issues_by_date['open']
    closedIssues = num_issues_by_date['closed']
    timeSeriesOpen = go.Scatter(x=openIssues[0], y=openIssues[1], line={'color':'firebrick'}, name="Open")
    timeSeriesClosed =  go.Scatter(x=closedIssues[0], y=closedIssues[1], line={'color':'royalblue'}, name="Closed")
    timeSeries = go.Figure(data=[timeSeriesOpen, timeSeriesClosed])
    timeSeries.update_layout(transition_duration=1000, title="Number of Daily Issues")
    
    return [timeSeries]
    
    


@app.callback(
    [
     Output('top-labels', 'figure'),
     Output('bar-plot', 'figure'),
     Output('pie-chart', 'figure'),
     ],
    [Input('data', 'children'),

     ])
def charts(jsonified_cleaned_data):
    
    
    # df = datum
    # data = gitAnalysis.indexByDateRange(df, start_date, end_date)
    # print(jsonified_cleaned_data);
    data = pd.read_json(jsonified_cleaned_data)
    num_issues_by_date = gitAnalysis.numofIssuesByDate(data)
    
    openIssues = num_issues_by_date['open']
    closedIssues = num_issues_by_date['closed']
    timeSeriesOpen = go.Scatter(x=openIssues[0], y=openIssues[1], line={'color':'firebrick'}, name="Open")
    timeSeriesClosed =  go.Scatter(x=closedIssues[0], y=closedIssues[1], line={'color':'royalblue'}, name="Closed")
    timeSeries = go.Figure(data=[timeSeriesOpen, timeSeriesClosed])
    timeSeries.update_layout(transition_duration=1000, title="Number of Daily Issues")
    
    label_count = gitAnalysis.getTop10Labels(data)
    fig = px.bar(label_count, x=label_count['label'].to_numpy()[:10], 
                     y=label_count['count'].to_numpy()[:10])
    fig.update_layout(transition_duration=1000, title="Top 10 Used Labels")
    
    stackLayers = gitAnalysis.getIssuesStacked(data)
    barChartStacks = []
    for layer in stackLayers:
        stack = go.Bar(
            y=layer['labels'],
            x=layer['data'],
            name=layer['name'],
            orientation="h"
        )
        barChartStacks.append(stack)
    barChart = go.Figure(data=barChartStacks,
                                layout=go.Layout(barmode='stack', title="Issue Breakdown"))
    barChart.update_layout(transition_duration=1000, title="Issue Breakdown")
    
    pieData = gitAnalysis.pieTop10Labels(data)
    pieChart = px.pie(pieData, names=pieData['label'], values=pieData['count'])
    pieChart.update_layout(transition_duration=1000, title="Percentage of Total Issues per Label")
    
    # assigneeList = gitAnalysis.getAssigneeList(data)
    # assignee_df = gitAnalysis.getAssigneeIssues(data, value)
    
    # stackLayers2 = gitAnalysis.getIssuesStacked(assignee_df)
    # barChartStacks2 = []
    # for layer in stackLayers2:
    #     stack = go.Bar(
    #         y=layer['labels'],
    #         x=layer['data'],
    #         name=layer['name'],
    #         orientation="h"
    #     )
    #     barChartStacks2.append(stack)
    # barChart2 = go.Figure(data=barChartStacks2,
    #                             layout=go.Layout(barmode='stack', title="Issue Breakdown"))
    # barChart2.update_layout(transition_duration=1000, title="Team Member Issue Breakdown")
    
    
    return fig, barChart, pieChart




# df = pd.read_csv("dap-planning.csv", converters={"label": ast.literal_eval,
#                                                   # "assignees": ast.literal_eval})
@app.callback(
        [Output('dropdown', 'options'),
          Output('pie-chart2', 'figure'),
          ],
          [  
          Input('data', 'children'),
          Input('dropdown', 'value')
          ]
    )
def assigneeCharts(jsonified_cleaned_data, value):
    # print(jsonified_cleaned_data[0][0])
    data = pd.read_json(jsonified_cleaned_data)
    assigneeList = gitAnalysis.getAssigneeList(data)
    assignee_df = gitAnalysis.getAssigneeIssues(data, value)
    
    stackLayers2 = gitAnalysis.getIssuesStacked(assignee_df)
    barChartStacks2 = []
    for layer in stackLayers2:
        stack = go.Bar(
            y=layer['labels'],
            x=layer['data'],
            name=layer['name'],
            orientation="h"
        )
        barChartStacks2.append(stack)
    barChart2 = go.Figure(data=barChartStacks2,
                                layout=go.Layout(barmode='stack', title="Issue Breakdown"))
    barChart2.update_layout(transition_duration=1000, title="Team Member Issue Breakdown")
    
    return assigneeList, barChart2
    

if __name__ == '__main__':
    app.run_server(debug=True)
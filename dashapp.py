#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from config import Config

# Data Collection Part
from app import app, db
from app.models import Project, TimeRecord
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

TASKTYPES = Config.TASKTYPES
JST = timezone(timedelta(hours=+9), 'JST')
requesteddate = datetime.now(JST).date()
weekdaynum = requesteddate.weekday()

# Default Dash Color Pallet
color_list = ['rgb(31, 119, 180)',
              'rgb(255, 127, 14)',
              'rgb(44, 160, 44)',
              'rgb(214, 39, 40)',
              'rgb(148, 103, 189)',
              'rgb(140, 86, 75)',
              'rgb(227, 119, 194)',
              'rgb(127, 127, 127)',
              'rgb(188, 189, 34)',
              'rgb(23, 190, 207)'
              ]

# DASH
dashapp = dash.Dash(name='app1', server=app, url_base_pathname='/app1/')


def server_layout():
    return html.Div(
        children=[
            html.H1('Weekly Report',),
            dcc.Graph(id="weekly-workload"),
            dcc.Graph(id="weekly-taskbalance"),
            dcc.Graph(id="weekly-projectbalance"),
            dcc.Interval(
                id='interval-component',
                interval=1000,  # in milliseconds
                n_intervals=0
            )
        ]
    )


dashapp.layout = server_layout()


@dashapp.callback([Output('weekly-workload', 'figure'),
                   Output('weekly-taskbalance', 'figure'),
                   Output("weekly-projectbalance", 'figure')],
                  [Input('interval-component', 'n_intervals')])
def update_graphs(n):
    result = {}
    dash_data = []
    task_balance = []
    for task_id, task in enumerate(TASKTYPES):
        result[task] = []
        task_record = TimeRecord.query.filter_by(tasktype=task)

        # Sum of each task type
        tasktime_by_week = task_record.filter(TimeRecord.starttime > requesteddate - timedelta(weekdaynum),
                                              TimeRecord.starttime < requesteddate + timedelta(1)
                                              )
        task_balance.append(sum([record.minutes for record in tasktime_by_week.all()]) / 60)

        # Work time of each day
        for i in range(weekdaynum, -1, -1):
            tasktimelist_by_day = task_record.filter(TimeRecord.starttime > requesteddate - timedelta(i),
                                                     TimeRecord.starttime < requesteddate - timedelta(i - 1)
                                                     )
            tasktime_by_day = sum([record.minutes for record in tasktimelist_by_day.all()]) / 60
            result[task].append(tasktime_by_day)

        dash_data.append(go.Bar(x=result[task],
                                y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                                type='bar',
                                name=task,
                                marker={'color': color_list[task_id]},
                                orientation='h',
                                ))

    dash_task_balance = go.Pie(labels=TASKTYPES,
                               values=task_balance,
                               marker={'colors': color_list},
                               sort=False,
                               )
    # Project Base
    project_balance = []
    project_list = [project for project in Project.query.filter_by(projectstatus=True)]
    for project in project_list:
        project_record = TimeRecord.query.filter_by(projectid=project.projectid)
        projecttime_by_week = project_record.filter(TimeRecord.starttime > requesteddate - timedelta(weekdaynum),
                                                    TimeRecord.starttime < requesteddate
                                                    )
        project_balance.append(sum([record.minutes for record in projecttime_by_week.all()]) / 60)

    dash_project_balance = go.Pie(labels=[project.projectname for project in project_list], values=project_balance)

    figure1 = {'data': dash_data,
               'layout': {'title': 'Weekly Workload',
                          'barmode': 'stack'}}

    figure2 = {'data': [dash_task_balance],
               'layout': {'title': 'Task Balance'}}

    figure3 = {'data': [dash_project_balance],
               'layout': {'title': 'Project Balance'}}

    return [figure1, figure2, figure3]
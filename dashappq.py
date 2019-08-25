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
dashapp = dash.Dash(name='app2', server=app, url_base_pathname='/app2/')


def server_layout():
    return html.Div(
        children=[
            html.H1('Quarterly Report'),
            html.H2('Personal Status'),
            dcc.Slider(id='billable', min=0, max=100, step=1, marks={i: f'{i}' for i in range(0, 100, 10)}),
            dcc.Interval(
                id='interval-component',
                interval=1000,  # in milliseconds
                n_intervals=0
            )
        ]
    )


dashapp.layout = server_layout()


@dashapp.callback([Output('billable', 'value')],
                  [Input('interval-component', 'n_intervals')])
def update_graphs(n):
    return [80]

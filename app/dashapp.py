#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app

dashapp = dash.Dash(name='app1', server=app, url_base_pathname='/app1/')

dashapp.layout = html.Div(
   children =[
    html.H1('Hello Dash',),
    dcc.Graph(
        id="first-graph",
        figure={'data': [{'x': [1, 2],
                          'y': [50, 90],
                          'type': 'bar',
                          'name': 'A'},
                         {'x':[1,2],
                          'y':[70, 20],
                          'type': 'bar',
                          'name': 'B'}
                         ],
                'layout': {'title': 'Dash Test'}
                }
    )
   ]
)


#!/usr/bin/python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import time
import numpy as np

from threading import Lock

from Experiences import Experiences
from Settings import Settings

lock = Lock()

experiences = Experiences()
settings = Settings()

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Button('Refresh', id='refresh'),

    dcc.Markdown('''
        # This is an <h1> tag
        ## This is an <h2> tag
        ###### This is an <h6> tag
    ''', id='status'),

    dcc.Graph(id='example-graph'),
    dcc.Graph(id='example-graph2'),
])

@app.callback(
    dash.dependencies.Output(component_id='status', component_property='children'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_status(input_value):

    lock.acquire()

    experiences = Experiences()
    settings = Settings()

    lock.release()

    return 'Total Experiences: ' + str(len(experiences.timestamps))

@app.callback(
    dash.dependencies.Output(component_id='example-graph', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_div(input_value):

    lock.acquire()

    temperatures = experiences.states0[:,-1]
    timestamps = experiences.timestamps
    temperatures = experiences.temperatures
    targets = experiences.targets

    lock.release()

    return {
        'data': [
            go.Scatter(x = timestamps, y = temperatures, name = 'temperature'),
            go.Scatter(x = timestamps, y = experiences.targets, name = 'target'),
        ],
        'layout': go.Layout(
            title='Double Y Axis Example',
            yaxis=dict(title='temperature'),
        )
    }

@app.callback(
    dash.dependencies.Output(component_id='example-graph2', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_div2(input_value):

    lock.acquire()

    timestamps = experiences.timestamps
    powers = experiences.powers
    values = experiences.values[:,0]

    lock.release()

    return {
        'data': [
            go.Scatter(x = timestamps, y = powers, mode = 'markers', name = 'power', yaxis='y1'),
            go.Scatter(x = timestamps, y = values, name = 'value', yaxis='y2'),
        ],
        'layout': go.Layout(
            title='power level',
            yaxis=dict(title='value'),
            yaxis2=dict(
                title='power level',
                overlaying='y',
                side='right'
            )
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')

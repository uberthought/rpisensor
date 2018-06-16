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

    dcc.Graph(id='graph-2d'),
    dcc.Graph(id='graph-3d', style={'height': '50em'}),
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
    dash.dependencies.Output(component_id='graph-2d', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_div(input_value):

    lock.acquire()

    timestamps = experiences.timestamps
    temperatures = experiences.temperatures
    humidities = experiences.humidities

    lock.release()

    return {
        'data': [
            go.Scatter(x = timestamps, y = temperatures, name = 'temperature', yaxis = 'y1'),
            go.Scatter(x = timestamps, y = humidities, name = 'humidity', yaxis = 'y2'),
        ],
        'layout': go.Layout(
            title='2D Temperature, Humidity vs Time',
            yaxis=dict(title='Celcius'),
            yaxis2=dict(
                title='Relative Humidity',
                overlaying='y',
                side='right'
            )
        )
    }

@app.callback(
    dash.dependencies.Output(component_id='graph-3d', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_div2(input_value):

    lock.acquire()

    timestamps = experiences.timestamps
    temperatures = experiences.temperatures
    humidities = experiences.humidities

    lock.release()

    offsets = [x - timestamps[0] for x in timestamps]
    offsets = [x.total_seconds() for x in offsets]

    return {
        'data': [
            # go.Scatter(x = timestamps, y = powers, mode = 'markers', name = 'power', yaxis='y1'),
            # go.Scatter(x = timestamps, y = values, name = 'value', yaxis='y2'),
            # go.Scatter(x = timestamps, y = temperatures),
            # go.Scatter(x = timestamps, y = humidities),
            go.Scatter3d(x = offsets, y = humidities, z = temperatures, mode = 'markers'),
        ],
        'layout': go.Layout(
            title='3D Temperature, Humidity, Time',
            scene = dict(
                xaxis=dict(title='Seconds'),
                yaxis=dict(title='Relative Humidity'),
                zaxis=dict(title='Celcius'),
            )
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')

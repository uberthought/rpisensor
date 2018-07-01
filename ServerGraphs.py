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

experiences = Experiences('server_experiences')
experiences.load()

settings = Settings()

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Example Temperature and Humidity Sensor'),

    html.Div(children='''
        This is an example app that displays the results of temperature and humidity sensor collection.
    '''),

    html.Button('Refresh', id='refresh'),

    dcc.Markdown('''
        # This is an <h1> tag
        ## This is an <h2> tag
        ###### This is an <h6> tag
    ''', id='status'),

    dcc.Graph(id='graph-2d', style={'height': '20em'}),
    dcc.Graph(id='graph-pm-2d', style={'height': '20em'}),
    # dcc.Graph(id='graph-3d', style={'height': '50em'}),
])

@app.callback(
    dash.dependencies.Output(component_id='status', component_property='children'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_status(input_value):

    experiences = Experiences('server_experiences')
    experiences.load()

    total = len(experiences.timestamps)
    last = experiences.timestamps[-1]

    return 'Last Timestamp: ' + str(last) + '  Total: ' + str(total)

@app.callback(
    dash.dependencies.Output(component_id='graph-2d', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_div(input_value):

    timestamps = experiences.timestamps
    temperatures = experiences.temperatures
    humidities = experiences.humidities

    return {
        'data': [
            go.Scatter(x = timestamps, y = temperatures, name = 'temperature', yaxis = 'y1'),
            go.Scatter(x = timestamps, y = humidities, name = 'humidity', yaxis = 'y2'),
        ],
        'layout': go.Layout(
            title='2D Temperature, Humidity vs Time',
            yaxis=dict(title='C'),
            yaxis2=dict(
                title='%',
                overlaying='y',
                side='right'
            )
        )
    }

@app.callback(
    dash.dependencies.Output(component_id='graph-pm-2d', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_pm_div(input_value):

    timestamps = experiences.timestamps
    pm25s = experiences.pm25s
    pm10s = experiences.pm10s

    return {
        'data': [
            go.Scatter(x = timestamps, y = pm25s, name = 'PM2.5'),
            go.Scatter(x = timestamps, y = pm10s, name = 'PM10'),
        ],
        'layout': go.Layout(
            title='2D PM2.5, PM10 vs Time',
            yaxis=dict(title='µm'),
        )
    }

# @app.callback(
#     dash.dependencies.Output(component_id='graph-3d', component_property='figure'),
#     [dash.dependencies.Input('refresh', 'n_clicks')])
# def update_output_div2(input_value):

#     timestamps = experiences.timestamps
#     temperatures = experiences.temperatures
#     humidities = experiences.humidities

#     offsets = [x - timestamps[0] for x in timestamps]
#     offsets = [x.total_seconds() for x in offsets]

#     return {
#         'data': [
#             go.Scatter3d(x = offsets, y = humidities, z = temperatures, mode = 'markers'),
#         ],
#         'layout': go.Layout(
#             title='3D Temperature, Humidity, Time',
#             scene = dict(
#                 xaxis=dict(title='Seconds'),
#                 yaxis=dict(title='Relative Humidity'),
#                 zaxis=dict(title='Celcius'),
#             )
#         )
#     }

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')

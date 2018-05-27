#!/usr/bin/python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import time

from Experiences import Experiences

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Button('Refresh', id='refresh'),

    dcc.Graph(id='example-graph'),

    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

    # [dash.dependencies.Input('interval-component', 'n_intervals')])

@app.callback(
    dash.dependencies.Output(component_id='example-graph', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_div(input_value):
    experiences = Experiences()
    temperatures = experiences.states0[:,3]
    values = experiences.values[:,0]
    timestamps = experiences.timestamps

    targets = experiences.states0[:,0]
    targets = [Experiences.denormalize_temperature(x) for x in targets]

    temperatures = experiences.states0[:,3]
    temperatures = temperatures + targets

    return {
        'data': [
            # go.Scatter(x = timestamps, y = temperatures, mode = 'markers', name = 'sensor temperature'),
            # go.Scatter(x = timestamps, y = targets, mode = 'markers', name = 'target temperature'),
            # go.Scatter(x = timestamps, y = values, mode = 'markers', name = 'value'),

            go.Scatter(x = timestamps, y = experiences.temperatures, mode = 'markers', name = 'temperature'),
            go.Scatter(x = timestamps, y = experiences.humidities, mode = 'markers', name = 'humidity'),
            go.Scatter(x = timestamps, y = experiences.powers, mode = 'markers', name = 'power'),
            go.Scatter(x = timestamps, y = experiences.targets, mode = 'markers', name = 'target'),
            # go.Scatter(x = timestamps, y = experiences.outsides, mode = 'markers', name = 'outside'),

        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.1.178')
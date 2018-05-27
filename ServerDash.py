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

    dcc.Graph(id='example-graph2'),

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
            # go.Scatter(x = timestamps, y = experiences.humidities, name = 'humidity'),
            # go.Scatter(x = timestamps, y = experiences.outsides, name = 'outside'),
            go.Scatter(x = timestamps, y = experiences.temperatures, name = 'temperature'),
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
            go.Scatter(x = timestamps, y = experiences.powers, mode = 'markers', name = 'power', yaxis='y1'),
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
    app.run_server(debug=True, host='10.128.0.3')

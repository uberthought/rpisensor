#!/usr/bin/python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import time

from threading import Lock

from Experiences import Experiences
from network import Model
from Settings import Settings

from plotQ import plotQ
from plotState import plotState
from plotValue import plotValue

lock = Lock()

experiences = Experiences()
model = Model()
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
    dcc.Graph(id='plotQ'),
    dcc.Graph(id='plotState'),
    dcc.Graph(id='plotValue'),
])

@app.callback(
    dash.dependencies.Output(component_id='status', component_property='children'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_status(input_value):

    lock.acquire()

    experiences = Experiences()
    model = Model()
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

@app.callback(
    dash.dependencies.Output(component_id='plotQ', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_plotQ(input_value):
    
    lock.acquire()

    temperatures, off, low, high, ac = plotQ(model, experiences, settings)

    lock.release()

    return {
        'data': [
            go.Scatter(x = temperatures, y = off, name = 'off', line = dict(color='green')),
            # go.Scatter(x = temperatures, y = low, name = 'low', line = dict(color='yellow')),
            go.Scatter(x = temperatures, y = high, name = 'high', line = dict(color='red')),
            # go.Scatter(x = temperatures, y = ac, name = 'ac', line = dict(color='blue')),
        ],
        'layout': go.Layout(
            title='Q Network Output',
            xaxis=dict(title='temperature'),
            yaxis=dict(title='Q'),

        )
    }

@app.callback(
    dash.dependencies.Output(component_id='plotState', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_plotState(input_value):
    
    temperatures, predicted_off, predicted_low, predicted_high, predicted_ac = plotState(model, experiences, settings)

    return {
        'data': [
            go.Scatter(x = temperatures, y = predicted_off, mode = 'markers', name = 'off'),
            # go.Scatter(x = temperatures, y = predicted_low, mode = 'markers', name = 'low'),
            go.Scatter(x = temperatures, y = predicted_high, mode = 'markers', name = 'high'),
            # go.Scatter(x = temperatures, y = predicted_ac, mode = 'markers', name = 'ac'),
        ],
        'layout': go.Layout(
            title='State',
            xaxis=dict(title='temperature'),
            yaxis=dict(title='temperature'),
        )
    }

@app.callback(
    dash.dependencies.Output(component_id='plotValue', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_plotValue(input_value):
    
    temperatures, predicted_off, predicted_low, predicted_high, predicted_ac = plotValue(model, experiences, settings)

    return {
        'data': [
            go.Scatter(x = temperatures, y = predicted_off, mode = 'markers', name = 'off'),
            # go.Scatter(x = temperatures, y = predicted_low, mode = 'markers', name = 'low'),
            go.Scatter(x = temperatures, y = predicted_high, mode = 'markers', name = 'high'),
            # go.Scatter(x = temperatures, y = predicted_ac, mode = 'markers', name = 'ac'),
        ],
        'layout': go.Layout(
            title='Value',
            xaxis=dict(title='value'),
            yaxis=dict(title='temperature'),
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True, host='10.128.0.3')

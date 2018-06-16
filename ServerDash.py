#!/usr/bin/python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import time

from Experiences import Experiences
from network import Model
from Settings import Settings

from plotQ import plotQ
from plotState import plotState
from plotValue import plotValue

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Button('Refresh', id='refresh'),

    dcc.Graph(id='example-graph'),
    dcc.Graph(id='example-graph2'),
    dcc.Graph(id='plotQ'),
    # dcc.Graph(id='plotState'),
    # dcc.Graph(id='plotValue'),

    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

    # [dash.dependencies.Input('interval-component', 'n_intervals')])

@app.callback(
    dash.dependencies.Output(component_id='example-graph', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_div(input_value):
    experiences = Experiences()
    temperatures = experiences.states0[:,-1]
    values = experiences.values[:,0]
    timestamps = experiences.timestamps

    targets = experiences.states0[:,0]
    targets = [Experiences.denormalize_temperature(x) for x in targets]

    temperatures = experiences.states0[:,-1]
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
    temperatures = experiences.states0[:,-1]
    values = experiences.values[:,0]
    timestamps = experiences.timestamps

    targets = experiences.states0[:,0]
    targets = [Experiences.denormalize_temperature(x) for x in targets]

    temperatures = experiences.states0[:,-1]
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

@app.callback(
    dash.dependencies.Output(component_id='plotQ', component_property='figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def update_output_plotQ(input_value):
    
    experiences = Experiences()
    model = Model()
    settings = Settings()

    temperatures, off, low, high, ac = plotQ(model, experiences, settings)

    return {
        'data': [
            go.Scatter(x = temperatures, y = off, name = 'off'),
            go.Scatter(x = temperatures, y = low, name = 'low'),
            go.Scatter(x = temperatures, y = high, name = 'high'),
            go.Scatter(x = temperatures, y = ac, name = 'ac'),
        ],
        'layout': go.Layout(
            title='plotQ'
        )
    }

# @app.callback(
#     dash.dependencies.Output(component_id='plotState', component_property='figure'),
#     [dash.dependencies.Input('refresh', 'n_clicks')])
# def update_output_plotState(input_value):
    
#     experiences = Experiences()
#     model = Model()
#     settings = Settings()

#     temperatures, predicted_off, predicted_low, predicted_high, predicted_ac = plotState(model, experiences, settings)

#     return {
#         'data': [
#             go.Scatter(x = temperatures, y = predicted_off, mode = 'markers', name = 'off'),
#             go.Scatter(x = temperatures, y = predicted_low, mode = 'markers', name = 'low'),
#             go.Scatter(x = temperatures, y = predicted_high, mode = 'markers', name = 'high'),
#             go.Scatter(x = temperatures, y = predicted_ac, mode = 'markers', name = 'ac'),
#         ],
#         'layout': go.Layout(
#             title='plotState'
#         )
#     }

# @app.callback(
#     dash.dependencies.Output(component_id='plotValue', component_property='figure'),
#     [dash.dependencies.Input('refresh', 'n_clicks')])
# def update_output_plotValue(input_value):
    
#     experiences = Experiences()
#     model = Model()
#     settings = Settings()

#     temperatures, predicted_off, predicted_low, predicted_high, predicted_ac = plotValue(model, experiences, settings)

#     return {
#         'data': [
#             go.Scatter(x = temperatures, y = predicted_off, mode = 'markers', name = 'off'),
#             go.Scatter(x = temperatures, y = predicted_low, mode = 'markers', name = 'low'),
#             go.Scatter(x = temperatures, y = predicted_high, mode = 'markers', name = 'high'),
#             go.Scatter(x = temperatures, y = predicted_ac, mode = 'markers', name = 'ac'),
#         ],
#         'layout': go.Layout(
#             title='plotState'
#         )
#     }


if __name__ == '__main__':
    app.run_server(debug=True, host='10.128.0.3')

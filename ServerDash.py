#!/usr/bin/python3

from threading import Thread

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import time

from Experiences import Experiences
from Communication import Communication

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Button('Refresh', id='refresh'),

    dcc.Graph(id='example-graph')
])

@app.callback(
    dash.dependencies.Output(component_id='example-graph', component_property='figure'),
    [dash.dependencies.Input(component_id='refresh', component_property='n_clicks')])
def update_output_div(input_value):
    experiences = Experiences()
    temperatures = experiences.states0[:,3]
    values = experiences.values[:,0]
    timestamps = experiences.timestamps[:,0]

    targets = experiences.states0[:,0]
    targets = [Experiences.denormalize_temperature(x) for x in targets]

    temperatures = experiences.states0[:,3]
    temperatures = temperatures + targets

    return {
        'data': [
            go.Scatter(x = timestamps, y = temperatures, mode = 'markers', name = 'sensor temperature'),
            go.Scatter(x = timestamps, y = targets, mode = 'markers', name = 'target temperature'),
            go.Scatter(x = timestamps, y = values, mode = 'markers', name = 'value'),
        ],
        # 'data': [
        #     {'x': timestamps, 'y': temperatures, 'type': 'scatter', 'name': 'temperatures'},
        #     {'x': timestamps, 'y': targets, 'type': 'scatter', 'name': 'targets'},
        #     {'x': timestamps, 'y': values, 'type': 'scatter', 'name': 'values'},
        # ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }

communication = Communication()
experiences = communication.receive_init('')

def collect():
    global communication

    while True:
        start = time.time()

        experiences = communication.receive('')
        experiences.append()

        elapse = time.time() - start
        print(elapse)

if __name__ == '__main__':
    webServerThread = Thread(target=app.run_server)
    # webServerThread = Thread(target=collect)
    webServerThread.start()

    collect()
    # app.run_server(debug=True)
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_3 = pd.read_excel("data/3_km.xls", sheet_name='3 KM')
df_10 = pd.read_excel("data/10_km.xls", sheet_name='10 KM')
df_21 = pd.read_excel("data/21_km.xls", sheet_name='21 KM')
df_42 = pd.read_excel("data/42_km.xls", sheet_name='42 KM')
df_nordic = pd.read_excel("data/nordic.xls", sheet_name='NORDIC')

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

#, 'columnCount': 2
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Almaty Marathon Visualization',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(
            id='dropdown-distance',
            options=[
                {'label': '3 KM', 'value': '3km'},
                {'label': '10 KM', 'value': '10km'},
                {'label': '21 KM', 'value': '21km'},
                {'label': '42 KM', 'value': '42km'},
                {'label': 'Скандинавская ходьба', 'value': 'nordic'}
            ],
            value='Выберите дистанцию'
    ),
    
    html.Div(id='heading-gender', children='Распределение участников по полу', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    
    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': ["10 km"], 'y': [len(df_10[df_10['Gender']=='M'])], 'type': 'bar', 'name': 'М'},
                {'x': ['10 km'], 'y': [len(df_10[df_10['Gender']=='F'])], 'type': 'bar', 'name': 'Ж'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
    ], style={'width': 500})

    

    # html.Label('Radio Items'),
    # dcc.RadioItems(
    #     options=[
    #         {'label': 'New York City', 'value': 'NYC'},
    #         {'label': u'Montréal', 'value': 'MTL'},
    #         {'label': 'San Francisco', 'value': 'SF'}
    #     ],
    #     value='MTL'
    # ),


    
])

@app.callback(
    Output(component_id='heading-gender', component_property='children'),
    [Input(component_id='dropdown-distance', component_property='value')]
)
def update_gender_graph(input_value):
    return input_value

if __name__ == '__main__':
    app.run_server(debug=True)
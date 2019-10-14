# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def age_group(df):
    if 0<=df<=18:
        return '0-18'
    elif 18<=df<34:
        return '18-34'
    elif 35<=df<49:
        return '35-49'
    elif 50<=df<59:
        return '50-59'
    else:
        return "60+"

df_3        = pd.read_excel("data/3_km.xls", sheet_name='3 KM')
df_10       = pd.read_excel("data/10_km.xls", sheet_name='10 KM')
df_21       = pd.read_excel("data/21_km.xls", sheet_name='21 KM')
df_42       = pd.read_excel("data/42_km.xls", sheet_name='42 KM')
df_nordic   = pd.read_excel("data/nordic.xls", sheet_name='NORDIC')

df_3['age_group']       = df_3['Age'].apply(age_group).value_counts()
df_10['age_group']      = df_10['Age'].apply(age_group).value_counts()
df_21['age_group']      = df_21['Age'].apply(age_group).value_counts()
df_42['age_group']      = df_42['Age'].apply(age_group).value_counts()
df_nordic['age_group']  = df_nordic['Age'].apply(age_group).value_counts()


colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# 'columnCount': 2
# "display": "inline-block", "textAlign": "center"
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Almaty Marathon Visualization',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
        
    dcc.Dropdown(style={'width': 500, 'margin': "0 auto"},
        id='dropdown-distance',
        options=[
            {'label': 'Скандинавская ходьба', 'value': 'nordic'},
            {'label': '3 KM', 'value': '3km'},
            {'label': '10 KM', 'value': '10km'},
            {'label': '21 KM', 'value': '21km'},
            {'label': '42 KM', 'value': '42km'}                    
        ],
        value="default",
        placeholder='Выберите дистанцию'
    ),
    
    # html.Div(id='heading-gender', children='Распределение участников по полу', style={
    #     'textAlign': 'center',
    #     'color': colors['text']
    # }),

    dcc.Graph(animate=True,
    config={'autosizable': True},
        id='gender-graph',
        figure={
            'data': [
                {'x': ["Выберите дистанцию"], 'y': [len(df_42[df_42['Gender']=='M'])], 'type': 'bar', 'name': 'Мужчины'},
                {'x': ['Выберите дистанцию'], 'y': [len(df_42[df_42['Gender']=='F'])], 'type': 'bar', 'name': 'Женщины'}
            ]
        },
        style={'width': 600, 'margin': "0 auto"}),

    dcc.Graph(animate=True,
    config={'autosizable': True},
        id='age-graph',
        figure={
            'data': [
                {'x': ["Выберите дистанцию"], 'y': [len(df_42[df_42['Gender']=='M'])], 'type': 'bar', 'name': 'Мужчины'},
                {'x': ['Выберите дистанцию'], 'y': [len(df_42[df_42['Gender']=='F'])], 'type': 'bar', 'name': 'Женщины'}
            ]
        },
        style={'width': 600, 'margin': "0 auto"})
    
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
    [Output(component_id='gender-graph', component_property='figure'),
    Output(component_id='age-graph', component_property='figure')],
    [Input(component_id='dropdown-distance', component_property='value')]
)
def update_graphs(input_value):
    # participants' gender countplot

    if input_value == "default":
        genders =  {"data": [{'x': ["Выберите дистанцию"], 'y': [1], 'type': 'bar', 'name': 'Мужчины'},
                {'x': ["Выберите дистанцию"], 'y': [1], 'type': 'bar', 'name': 'Женщины'}]}
    elif input_value == "nordic":
        genders = {"data": [{'x': ["Скандинавская ходьба"], 'y': [len(df_nordic[df_nordic['Gender']=='M'])], 'type': 'bar', 'name': 'Мужчины'},
                        {'x': ["Скандинавская ходьба"], 'y': [len(df_nordic[df_nordic['Gender']=='F'])], 'type': 'bar', 'name': 'Женщины'}],
                'layout': {'yaxis': {'range': [0, 400]}}}
    elif input_value == "3km":
        genders =  {"data": [{'x': [input_value], 'y': [0], 'type': 'bar', 'name': 'Мужчины'},
                        {'x': [input_value], 'y': [0], 'type': 'bar', 'name': 'Женщины'}]}
    elif input_value == "10km":
        genders = {"data": [{'x': [input_value], 'y': [len(df_10[df_10['Gender']=='M'])], 'type': 'bar', 'name': 'Мужчины'},
                        {'x': [input_value], 'y': [len(df_10[df_10['Gender']=='F'])], 'type': 'bar', 'name': 'Женщины'}],
                'layout': {'yaxis': {'range': [0, 4500]}}}
    elif input_value == "21km":
        genders = {"data": [{'x': [input_value], 'y': [len(df_21[df_21['Gender']=='M'])], 'type': 'bar', 'name': 'Мужчины'},
                        {'x': [input_value], 'y': [len(df_21[df_21['Gender']=='F'])], 'type': 'bar', 'name': 'Женщины'}],
                'layout': {'yaxis': {'range': [0, 3000]}}}

    elif input_value == "42km":
        genders = {"data": [{'x': [input_value], 'y': [len(df_42[df_42['Gender']=='M'])], 'type': 'bar', 'name': 'Мужчины'},
                        {'x': [input_value], 'y': [len(df_42[df_42['Gender']=='F'])], 'type': 'bar', 'name': 'Женщины'}],
                'layout': {'yaxis': {'range': [0, 1000]}}}
        
    return genders, genders
    
if __name__ == '__main__':
    app.run_server(debug=True)
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import random

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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

df_3['age_group']       = df_3['Age'].apply(age_group)
df_10['age_group']      = df_10['Age'].apply(age_group)
df_21['age_group']      = df_21['Age'].apply(age_group)
df_42['age_group']      = df_42['Age'].apply(age_group)
df_nordic['age_group']  = df_nordic['Age'].apply(age_group)

df_3['Разворот']                        = pd.to_timedelta(df_3['Разворот'])
df_3['Чип время']                       = pd.to_timedelta(df_3['Чип время'])
df_10['2.27 km Аль-Фараби Достык']      = pd.to_timedelta(df_10['2.27 km Аль-Фараби Достык'])
df_10['Gun Time']                       = pd.to_timedelta(df_10['Gun Time'])
df_21['8.0 km ППП']                     = pd.to_timedelta(df_21['8.0 km ППП'])
df_21['12.0 km Абая Саина']             = pd.to_timedelta(df_21['12.0 km Абая Саина'])
df_21['Gun Time']                       = pd.to_timedelta(df_21['Gun Time'])
df_42['8.0 km ППП']                     = pd.to_timedelta(df_42['8.0 km ППП'])
df_42['12.0 km Абая Саина']             = pd.to_timedelta(df_42['12.0 km Абая Саина'])
df_42['21.0 km Площадь Республики']     = pd.to_timedelta(df_42['21.0 km Площадь Республики'])
df_42['29.0 km ППП']                    = pd.to_timedelta(df_42['29.0 km ППП'])
df_42['33.0 km Абая Саина']             = pd.to_timedelta(df_42['33.0 km Абая Саина'])
df_42['Gun Time']                       = pd.to_timedelta(df_42['Gun Time'])

df_10['Gun Time'] = df_10['Gun Time'].dt.seconds/60
df_21['Gun Time'] = df_21['Gun Time'].dt.seconds/60
df_42['Gun Time'] = df_42['Gun Time'].dt.seconds/60
df_10['tt'] = 30
df_21['tt'] = 30
df_42['tt'] = 30


colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

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
        id='age-graph',
        figure={
            'data': [
                {'x': ["Выберите дистанцию"], 'y': [len(df_42[df_42['Gender']=='M'])], 'type': 'bar', 'name': 'Мужчины'},
                {'x': ['Выберите дистанцию'], 'y': [len(df_42[df_42['Gender']=='F'])], 'type': 'bar', 'name': 'Женщины'}
            ]
        },
        style={'width': 600, 'margin': "0 auto"}),

    dcc.Graph(id='gender-graph',
            style={'width': 600, 'margin': "0 auto"}),

    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=0,
        max=12,
        value=0,
        marks={
            0: '0',
            1: '30',
            2: '60',
            3: '90',
            4: '120',
            5: '150',
            6: '180',
            7: '210',
            8: '240',
            9: '270',
            10: '300',
            11: '330',
            12: '360'
        },
        step=None
    )

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')]
)
def update_time_graph(input_value):
    traces = []

    print(input_value)
    traces.append(go.Scatter(
            name="10 км",
            x=df_10['tt']*input_value,
            y=100*df_10['tt']*input_value/df_10['Gun Time'],
            text=df_10['Стартовый'],
            mode='markers',
            opacity=0.7,
            marker={
                'color': 'green',
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ))

    traces.append(go.Scatter(
            name="21 км",
            x=df_21['tt']*input_value,
            y=100*df_21['tt']*input_value/df_21['Gun Time'],
            text=df_21['Стартовый'],
            mode='markers',
            opacity=0.7,
            marker={
                'color': 'blue',
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ))

    traces.append(go.Scatter(
            name="42 км",
            x=df_42['tt']*input_value,
            y=100*df_42['tt']*input_value/df_42['Gun Time'],
            text=df_42['Стартовый'],
            mode='markers',
            opacity=0.7,
            marker={
                'color': 'red',
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Прогресс по времени в минутах', 'range': [0, 360]},
            yaxis={'title': '% завершения трассы', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

@app.callback(
    Output(component_id='gender-graph', component_property='figure'),
    [Input(component_id='dropdown-distance', component_property='value')]
)
def update_gender_graph(input_value):
    if input_value == "default":
        genders = {"data": [go.Pie(labels=['Мужчины', 'Женщины'], values=[1, 1],
                        marker={'colors': ['#c93232', '#c93232']}, textinfo='none')],
                "layout": go.Layout(title="Выберите дистанцию")}
    elif input_value == "nordic":
        genders = {"data": [go.Pie(labels=['Мужчины', 'Женщины'], values=[len(df_21[df_21['Gender']=='M']), len(df_21[df_21['Gender']=='F'])],
                        marker={'colors': ['#3b8cef', '#c93232']}, textinfo='none')],
                "layout": go.Layout(title="Статистика участников по полу")}
    elif input_value == "3km":
        genders = {"data": [go.Pie(labels=['Мужчины', 'Женщины'], values=[1, 1],
                        marker={'colors': ['#d4d2d2', '#d4d2d2']}, textinfo='none')],
                "layout": go.Layout(title="Статистика участников по полу")}
    elif input_value == "10km":
        genders = {"data": [go.Pie(labels=['Мужчины', 'Женщины'], values=[len(df_10[df_10['Gender']=='M']), len(df_10[df_10['Gender']=='F'])],
                        marker={'colors': ['#3b8cef', '#c93232']}, textinfo='none')],
                "layout": go.Layout(title="Статистика участников по полу")}
    elif input_value == "21km":
        genders = {"data": [go.Pie(labels=['Мужчины', 'Женщины'], values=[len(df_21[df_21['Gender']=='M']), len(df_21[df_21['Gender']=='F'])],
                        marker={'colors': ['#3b8cef', '#c93232']}, textinfo='none')],
                "layout": go.Layout(title="Статистика участников по полу")}
    elif input_value == "42km":
        genders = {"data": [go.Pie(labels=['Мужчины', 'Женщины'], values=[len(df_42[df_42['Gender']=='M']), len(df_42[df_42['Gender']=='F'])],
                        marker={'colors': ['#3b8cef', '#c93232']}, textinfo='none')],
                "layout": go.Layout(title="Статистика участников по полу")}
    return genders

@app.callback(
    Output(component_id='age-graph', component_property='figure'),
    [Input(component_id='dropdown-distance', component_property='value')]
)
def update_age_graphs(input_value):
    # participants' gender countplot
    if input_value == "default":
        age_groups = {"data": [{'x': ["Выберите дистанцию"], 'y': [1], 'type': 'bar', 'name': '0-18'},
                        {'x': ["Выберите дистанцию"], 'y': [1], 'type': 'bar', 'name': '18-34'},
                        {'x': ["Выберите дистанцию"], 'y': [1], 'type': 'bar', 'name': '35-49'},
                        {'x': ["Выберите дистанцию"], 'y': [1], 'type': 'bar', 'name': '50-59'},
                        {'x': ["Выберите дистанцию"], 'y': [1], 'type': 'bar', 'name': '60+'}],
                'layout': {'yaxis': {'range': [0, 1000]}, 'title': "Распределение по возрасту"}}
    elif input_value == "nordic":
        age_groups = {"data": [{'x': [input_value], 'y': [len(df_nordic[df_nordic['age_group']=='0-18'])], 'type': 'bar', 'name': '0-18'},
                        {'x': [input_value], 'y': [len(df_nordic[df_nordic['age_group']=='18-34'])], 'type': 'bar', 'name': '18-34'},
                        {'x': [input_value], 'y': [len(df_nordic[df_nordic['age_group']=='35-49'])], 'type': 'bar', 'name': '35-49'},
                        {'x': [input_value], 'y': [len(df_nordic[df_nordic['age_group']=='50-59'])], 'type': 'bar', 'name': '50-59'},
                        {'x': [input_value], 'y': [len(df_nordic[df_nordic['age_group']=='60+'])], 'type': 'bar', 'name': '60+'}],
                'layout': {'yaxis': {'range': [0, 400]}}}
    elif input_value == "3km":
        age_groups = {"data": [{'x': [input_value], 'y': [0], 'type': 'bar', 'name': '0-18'},
                        {'x': [input_value], 'y': [0], 'type': 'bar', 'name': '18-34'},
                        {'x': [input_value], 'y': [0], 'type': 'bar', 'name': '35-49'},
                        {'x': [input_value], 'y': [0], 'type': 'bar', 'name': '50-59'},
                        {'x': [input_value], 'y': [0], 'type': 'bar', 'name': '60+'}],
                'layout': {'yaxis': {'range': [0, 1000]}}}
    elif input_value == "10km":
        age_groups = {"data": [{'x': [input_value], 'y': [len(df_10[df_10['age_group']=='0-18'])], 'type': 'bar', 'name': '0-18'},
                        {'x': [input_value], 'y': [len(df_10[df_10['age_group']=='18-34'])], 'type': 'bar', 'name': '18-34'},
                        {'x': [input_value], 'y': [len(df_10[df_10['age_group']=='35-49'])], 'type': 'bar', 'name': '35-49'},
                        {'x': [input_value], 'y': [len(df_10[df_10['age_group']=='50-59'])], 'type': 'bar', 'name': '50-59'},
                        {'x': [input_value], 'y': [len(df_10[df_10['age_group']=='60+'])], 'type': 'bar', 'name': '60+'}],
                'layout': {'yaxis': {'range': [0, 4500]}}}
    elif input_value == "21km":
        age_groups = {"data": [{'x': [input_value], 'y': [len(df_21[df_21['age_group']=='0-18'])], 'type': 'bar', 'name': '0-18'},
                        {'x': [input_value], 'y': [len(df_21[df_21['age_group']=='18-34'])], 'type': 'bar', 'name': '18-34'},
                        {'x': [input_value], 'y': [len(df_21[df_21['age_group']=='35-49'])], 'type': 'bar', 'name': '35-49'},
                        {'x': [input_value], 'y': [len(df_21[df_21['age_group']=='50-59'])], 'type': 'bar', 'name': '50-59'},
                        {'x': [input_value], 'y': [len(df_21[df_21['age_group']=='60+'])], 'type': 'bar', 'name': '60+'}],
                'layout': {'yaxis': {'range': [0, 3000]}}}

    elif input_value == "42km":
        age_groups = {"data": [{'x': [input_value], 'y': [len(df_42[df_42['age_group']=='0-18'])], 'type': 'bar', 'name': '0-18'},
                        {'x': [input_value], 'y': [len(df_42[df_42['age_group']=='18-34'])], 'type': 'bar', 'name': '18-34'},
                        {'x': [input_value], 'y': [len(df_42[df_42['age_group']=='35-49'])], 'type': 'bar', 'name': '35-49'},
                        {'x': [input_value], 'y': [len(df_42[df_42['age_group']=='50-59'])], 'type': 'bar', 'name': '50-59'},
                        {'x': [input_value], 'y': [len(df_42[df_42['age_group']=='60+'])], 'type': 'bar', 'name': '60+'}],
                'layout': {'yaxis': {'range': [0, 1000]}}}
        
    return age_groups
    
if __name__ == '__main__':
    app.run_server(debug=True)
# -*- coding: utf-8 -*-

# Run this app with `python NBA Analytics 2010-2021.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#! pip install dash
#! pip install jupyter-dash
#! pip install pandas

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import pandas as pd

#NBA Players
df = pd.read_csv('NBA Data/NBA_Player_df.csv')
#NBA Teams
tdf = pd.read_csv('NBA Data/NBA_Stats_2010-11_2020-21.csv')
#Stepwise predictions
df1 = pd.read_csv('NBA Data/stepwise.csv')
#Hand Picked Predictions
df2 = pd.read_csv('NBA Data/Handpicked.csv')

# Figures
fig1 = px.scatter(df1, x=df1['Preds'], y=df1['W'],title="Step-Wise RMSE(2.618) R^2(0.954)", height=500)

fig2 = px.scatter(df2, x=df2['Preds'], y=df2['W'],title="Hand Picked Stats RMSE(4.359) R^2(0.874)", height=500)

available_indicators = tdf['Team'].unique()

available_indicators2 = df['Player'].unique()

app = JupyterDash(__name__)

markdown_title = '''
### NBA Analytics And Predictions

'''

markdown_text = '''
### NBA Season Long Win Predictions
Step-Wise Stats Chosen:
# 
    PTS -- Points
    3PA -- 3-Point Field Goal Attempts
    2PA -- 2-point Field Goal Attempts
    NRtg -- Net Rating; an estimate of point differential per 100 possessions.
    PW -- Pythagorean wins, i.e., expected wins based on points scored and allowed
    FG% -- Field Goal Percentage
    ORtg -- Offensive Rating
    DRtg -- Defensive Rating
    ORB -- Offensive Rebounds
    DRB -- Defensive Rebounds
'''
markdown_texts = '''
Hand Picked Stats Chosen:
#
    FTA -- Free Throw Attempts
    3PA -- 3-Point Field Goal Attempts
    2PA -- 2-point Field Goal Attempts
    FGA -- Field Goal Attempts
    ORB% -- Offensive Rebound Percentage
    DRB% -- Defensive Rebound Percentage
    ORtg -- Offensive Rating
    DRtg -- Defensive Rating
    TOV% -- Opponent Turnover Percentage
    STL -- Steals
    BLK -- Blocks
'''
markdown_text2 = '''
### Most Similar NBA Players By Year and Position With Points Per Game
'''

markdown_text3 = '''
### Most Similar NBA Players By Year Clustered
'''
markdown_text4 = '''
### Most Similar NBA Players By Year and Position With Minutes Played Per Game
'''

app.layout = html.Div([
        ####
    dcc.Markdown(children=markdown_title),
        html.Div([
            dcc.Dropdown(
                id='team_drop',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Boston Celtics'
            )
        ],
        style={'width': '18%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='team_drop2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Denver Nuggets'
            )
        ],
        style={'width': '18%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic'),

        ####
        html.Div([
            dcc.Dropdown(
                id='team_drop3',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Boston Celtics'
            )
        ],
        style={'width': '18%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='team_drop4',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Denver Nuggets'
            )
        ],
        style={'width': '18%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic3'),
        ####
        html.Div([
            dcc.Dropdown(
                id='Player_drop',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='LeBron James'
            )
        ],
        style={'width': '18%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='Player_drop2',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='Stephen Curry'
            )
        ],
        style={'width': '18%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic2'),

    dcc.Markdown(children=markdown_text3),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),
    dcc.Markdown(children=markdown_text2),
    dcc.Graph(id='graph2-with-slider'),
    dcc.Slider(
        id='year-slider2',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),

    dcc.Markdown(children=markdown_text4),
    dcc.Graph(id='graph3-with-slider'),
    dcc.Slider(
        id='year-slider3',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),

    dcc.Markdown(children=markdown_text),
    dcc.Graph(
        id='step-wise',
        figure=fig1),

    dcc.Markdown(children=markdown_texts),
    dcc.Graph(
        id='hand-wise',
        figure=fig2),
])
####
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('team_drop', 'value'),
    Input('team_drop2', 'value'))

def update_graph(team_drop, team_drop2):
    dff = tdf[tdf['Team'] == team_drop]
    dfs = tdf[tdf['Team'] == team_drop2]

    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Line(x=dff['Year'], y=dff['W/L%']),row=1, col=1)

    fig.add_trace(
        go.Line(x=dfs['Year'], y=dfs['W/L%']),row=1, col=2)

    fig.update_layout(height=600, width=1400, title_text="NBA Teams Win/Loss Comparison")     

    return fig

@app.callback(
    Output('indicator-graphic3', 'figure'),
    Input('team_drop3', 'value'),
    Input('team_drop4', 'value'))

def update_graph2(team_drop3, team_drop4):
    dff = tdf[tdf['Team'] == team_drop3]
    dfs = tdf[tdf['Team'] == team_drop4]

    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Line(x=dff['Year'], y=dff['3PA']),row=1, col=1)

    fig.add_trace(
        go.Line(x=dfs['Year'], y=dfs['3PA']),row=1, col=2)

    fig.update_layout(height=600, width=1400, title_text="NBA Teams 3 Point Attempts Comparison Over The Years")     

    return fig

@app.callback(
    Output('indicator-graphic2', 'figure'),
    Input('Player_drop', 'value'),
    Input('Player_drop2', 'value'))

def update_graph(Player_drop, Player_drop2):
    dff = df[df['Player'] == Player_drop]
    dfs = df[df['Player'] == Player_drop2]

    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Line(x=dff['Year'], y=dff['3P%']),row=1, col=1)

    fig.add_trace(
        go.Line(x=dfs['Year'], y=dfs['3P%']),row=1, col=2)

    fig.update_layout(height=600, width=1400, title_text="NBA Player 3 Point Percentage Comparison") 

    return fig

#####
@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))

def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]

    filtered_df['cluster'] = filtered_df['cluster'].astype(str)

    fig = px.scatter(filtered_df, x="x_cor", y="y_cor",
                     color="cluster",hover_name=filtered_df['Player']
                     )

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('graph2-with-slider', 'figure'),
    Input('year-slider2', 'value'))

def update_figure2(selected_year):
    filtered_df = df[df.Year == selected_year]

    fig = px.scatter(filtered_df, x="x_cor", y="y_cor",
                     color="Pos", size='PTS', hover_name=filtered_df['Player']
                     )

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('graph3-with-slider', 'figure'),
    Input('year-slider3', 'value'))

def update_figure3(selected_year):
    filtered_df = df[df.Year == selected_year]

    fig = px.scatter(filtered_df, x="x_cor", y="y_cor",
                     color="Pos", size='MP', hover_name=filtered_df['Player']
                     )

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
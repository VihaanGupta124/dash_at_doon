# from msilib.schema import Component
from optparse import Values
from turtle import width
import dash
import plotly.express as px
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import base64


def CardContent(heading, callback_output):
    card_content = [
        dbc.CardHeader(heading),
        dbc.CardBody(
            [
                html.H1(""),
                html.H1(id=callback_output, className="card-title"),
            ]
        ),
    ]
    return card_content


df = pd.read_csv("data/sample.csv")

df = df[df['curriculum'] == 'IB']

image_filename = 'data/doon_logo.jpeg'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.H1("Student Performance Analysis")),
            dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image)))

        ]
    ),
    dcc.Dropdown(id='subject-score',
                 options=[{'label': x, 'value': x}
                          for x in sorted(df.subject.unique())],
                 value='Mathematics',
                 style={
                    'width': '50%'
                 }),

    dbc.Row([
        dbc.Col(
            [
                dbc.Card(
                    CardContent(heading="Subject Average",
                                callback_output="average-subject-score"),
                    color="primary", inverse=True
                ),
                html.H1(""),
                dbc.Card(
                    CardContent(heading="Subject Median",
                                callback_output="median-subject-score"),
                    color="primary", inverse=True
                )
            ],
            style={
                'padding': 50,
                # 'margin-top': 50
            }
        ),
        dbc.Col(
            dcc.Graph(id='my-graph'), width={'size': 6},

            style={
                # 'padding': -50,
                'margin-top': -25
            },
        )
    ])
])


########################################
# Callbacks
########################################


@ app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='subject-score', component_property='value'),
)
def interactive_graphing(value_genre):
    print(value_genre)
    dff = df[df.subject == value_genre]
    print(dff)
    fig = px.histogram(data_frame=dff,  x='score', nbins=7)
    return fig


@ app.callback(
    Output(component_id='average-subject-score',
           component_property='children'),
    Input(component_id='subject-score', component_property='value'),
)
def average_score(value_genre):
    dff = df[df.subject == value_genre]
    print(dff.score.mean())
    return round(dff.score.mean(), 2)


@ app.callback(
    Output(component_id='median-subject-score',
           component_property='children'),
    Input(component_id='subject-score', component_property='value'),
)
def median_score(value_genre):
    dff = df[df.subject == value_genre]
    print(dff.score.median())
    return round(dff.score.median(), 2)


if __name__ == '__main__':
    app.run_server()

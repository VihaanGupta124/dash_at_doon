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
import dash_daq as daq
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

max_year = max(df.year)
# df = df[df['curriculum'] == 'IB']

# image_filename = 'data/doon_logo.jpeg'  # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.H1("     ")),
            dbc.Col(
                html.H1("Student Performance Analysis"),
                width={"size": 6, "offset": 2},),
            # dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image)))
            dbc.Col(html.H1("     ")),

        ]
    ),
    daq.BooleanSwitch(id="curriculum_toggle",
                      on=True,
                      label="ISC---------IB",
                      labelPosition="top",

                      style={
                          'margin-left': '0%',
                          'padding': '2.5%'
                      }),
    dbc.Row
    ([
        dbc.Col(

        ),
        dbc.Col(
            dcc.Dropdown(id='subject-score',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df.subject.unique())],
                         value='Mathematics',
                         style={
                             'width': '100%'
                            #  'padding': 50%

                         }),),
        dbc.Col(
            dcc.Dropdown(id='year',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df.year.unique())],
                         value=max_year,
                         style=dict(
                            width='100%',
                         )
                         )),
        dbc.Col()
    ]),
    dbc.Row([
        dbc.Col(
            [
                dbc.Card(
                    CardContent(heading="Subject Average",
                                callback_output="average-subject-score"),
                    color="dark", inverse=True
                ),
                html.H1(""),
                dbc.Card(
                    CardContent(heading="Subject Median",
                                callback_output="median-subject-score"),
                    color="dark", inverse=True
                )
            ],
            style={
                'padding': 50,
                'margin-top': 50
            }
        ),
        dbc.Col(
            dcc.Graph(id='my-graph'), width={'size': 6},

            style={
                # 'padding': -50,
                'margin-top': 25
            },
        )
    ]),

    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='yearly_score'), width={'size': 12},
                style={
                    # 'padding': -50,
                    'margin-top': '-2.7%'
                },

            )
        ]
    )
])


############################################################################################################
# Callbacks
############################################################################################################


def get_curriculum(toggle_bool):
    return ("IB", 7) if toggle_bool == True else ("ISC", 30)


@ app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='subject-score', component_property='value'),
    Input(component_id='year', component_property='value'),
    Input(component_id='curriculum_toggle', component_property='on')
)
def subject_histogram(subject, year, curriculum_toggle):
    print("--------SUBJECT HISTOGRAM-----------")
    print(subject)
    print(year)
    print(curriculum_toggle)
    curriculum, n_bins = get_curriculum(curriculum_toggle)
    df_subject = df[df.subject == subject]
    df_year = df_subject[df_subject.year == year]
    df_final = df_year[df_year.curriculum == curriculum]

    # df_final = df[
    #     (df.subject == subject) &
    #     (df.year == year) &
    #     (df.curriculum == get_curriculum(curriculum_toggle))
    # ]

    print(df_final)
    fig = px.histogram(data_frame=df_final,  x='score', nbins=n_bins)
    title_str = f'{subject} histogram for {year}'
    fig.update_layout(title_text=title_str, title_x=0.5)
    return fig


@ app.callback(
    Output(component_id='yearly_score', component_property='figure'),
    Input(component_id='subject-score', component_property='value'),
    Input(component_id='curriculum_toggle', component_property='on')

    # Input(component_id='year', component_property='value'),
)
def yearly_graph(subject, curriculum_toggle):
    print("--------YEARLY GRAPH-----------")
    print(subject)
    print(curriculum_toggle)
    curriculum, n_bins = get_curriculum(curriculum_toggle)
    dff = df[df.subject == subject]
    df_final = dff[dff.curriculum == curriculum]
    df_final = df_final.groupby(['year'])[['score']].mean().reset_index()
    print(df_final)
    fig = px.line(df_final, x="year", y='score')
    title2_str = f'{subject} timeseries'
    fig.update_layout(title_text=title2_str, title_x=0.5)

    return fig


@ app.callback(
    Output(component_id='average-subject-score',
           component_property='children'),
    Input(component_id='subject-score', component_property='value'),
    Input(component_id='year', component_property='value'),
    Input(component_id='curriculum_toggle', component_property='on')



)
def average_score(subject, year, curriculum_toggle):
    print("--------AVERAGE SCORE-----------")
    df_subject = df[df.subject == subject]
    df_year = df_subject[df_subject.year == year]
    curriculum, n_bins = get_curriculum(curriculum_toggle)
    df_final = df_year[df_year.curriculum == curriculum]
    print(df_final.score.mean())
    return round(df_final.score.mean(), 2)


@ app.callback(
    Output(component_id='median-subject-score',
           component_property='children'),
    Input(component_id='subject-score', component_property='value'),
    Input(component_id='year', component_property='value'),
    Input(component_id='curriculum_toggle', component_property='on')


)
def median_score(subject, year, curriculum_toggle):
    print("--------MEDIAN SCORE-----------")
    df_subject = df[df.subject == subject]
    df_year = df_subject[df_subject.year == year]
    curriculum, n_bins = get_curriculum(curriculum_toggle)
    df_final = df_year[df_year.curriculum == curriculum]
    print(df_final.score.median())
    return round(df_final.score.median(), 2)


if __name__ == '__main__':
    app.run_server()

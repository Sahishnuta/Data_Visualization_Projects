import dash

dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import numpy as np
import pandas as pd
from natsort import natsorted
import pathlib

def get_pandas_data(csv_filename: str) -> pd.DataFrame:
  
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath("data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(csv_filename))


df = get_pandas_data("aac_intakes_outcomes.csv")



layout = html.Div(
    [
     html.H1('Analyzing Time Spent in Shelter', style={'textAlign': 'center'}),
     html.P('In this analysis, we will analyze what factors may lead to an animal being in the shelter longer than others.', style={'textAlign': 'center'}),
     html.P('Graph takes a second to load!!!', style={'textAlign': 'center'}),
     
     
    html.P('Choose an X variable:'),
    dcc.Dropdown(['age_upon_intake_age_group', 'animal_type', 'intake_type', 'intake_condition', 'sex_upon_intake'], 'animal_type', id='y-dropdown'),
    dcc.Graph(id="histograms-graph"),
    ]
)


@callback(
    Output("histograms-graph", "figure"),
    Input("y-dropdown", "value"),
)
def display_color(category):
    order = df.groupby(by = category, level=0).mean().sort_values(by='time_in_shelter_days',ascending=False).index.to_list()
    fig = px.violin(df, y="time_in_shelter_days", points='all', box=True, x = category, category_orders={category: order})
    return fig
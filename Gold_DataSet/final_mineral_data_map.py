from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from PIL import Image
import numpy as np
from plotly.subplots import make_subplots
import collections
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
about_dataset= "Gold is a chemical element with the symbol Au (from Latin: aurum) and atomic number 79, making it one of the higher atomic number elements that occur naturally. It is a bright, slightly orange-yellow, dense, soft, malleable, and ductile metal in a pure form. Chemically, gold is a transition metal and a group 11 element. It is one of the least reactive chemical elements and is solid under standard conditions."


Top10GoldConsumers=pd.read_excel("GoldRankCountryWise.xlsx",sheet_name="Top10PopulationGoldHoldings")
Jwellery1021=pd.read_excel("GoldRankCountryWise.xlsx",sheet_name="Jwellery1021")
Gold2021=pd.read_excel("GoldRankCountryWise.xlsx",sheet_name="2021")
Gold2019=pd.read_excel("GoldRankCountryWise.xlsx",sheet_name="2019")
Gold1921 = pd.concat([Gold2021, Gold2019], axis=0)
Wd2021=pd.read_excel("GoldRankCountryWise.xlsx",sheet_name="GolddemandSummary")

fig1 = px.histogram(Top10GoldConsumers,y="Country",x="Tonnes",color=Top10GoldConsumers["Country"])
fig2 = px.histogram(Gold1921,y="Region",x="Gold Reserves Tonnes",color="Economic grouping")


fig3= go.Figure()
fig3.add_trace(go.Bar(x=Gold2021["Region"],y=Gold2021["Gold Reserves Tonnes"],name='Gold Reserves 2021',marker_color='indianred'))
fig3.add_trace(go.Bar(x=Gold2019["Region"],y=Gold2019["Gold Reserves Tonnes"],name='Gold Reserves 2019',marker_color='Blue'))

fig4 = go.Figure()
fig4.add_trace(go.Bar(x=Gold2021["Economic grouping"],y=Gold2021["Gold Reserves Tonnes"],name='Gold Reserves 2021',marker_color='indianred'))
fig4.add_trace(go.Bar(x=Gold2019["Economic grouping"],y=Gold2019["Gold Reserves Tonnes"],name='Gold Reserves 2019',marker_color='Blue'))


fig5 = px.treemap(Gold2021, path=[px.Constant("world"), 'Region','Country'], values='Total Reserves',
                  color='Gold Reserves Tonnes', hover_data=['Gold Reserves Tonnes'],
                  color_continuous_scale='RdBu'
                  )
fig5.update_layout(margin = dict(t=50, l=25, r=25, b=25))


fig7 = px.treemap(Gold2021, path=[px.Constant("world"), 'Country', 'Economic grouping'], values='Total Reserves',
                  color='Gold Reserves Tonnes', hover_data=['Gold Reserves Tonnes'],
                  color_continuous_scale='RdBu'
                  )
fig7.update_layout(margin = dict(t=50, l=25, r=25, b=25))


locator = Nominatim(user_agent= "myGeocoder")
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
Gold1921['location'] = Gold1921['City'].apply(geocode)
Gold1921['point'] = Gold1921['location'].apply(lambda loc: tuple(loc.point) if loc else None)
Gold1921[['latitude', 'longitude', 'altitude']] = pd.DataFrame(Gold1921['point'].tolist(), index=Gold1921.index)
fig11 = px.scatter_geo(Gold1921, lat= Gold1921['latitude'], lon = Gold1921['longitude'],
                     size="Gold Reserves Tonnes", color="Country")
fig11.show()


Portfolios = Wd2021["Field"]
Demand = Wd2021[2020]
fig10 = go.Figure(data=[go.Pie(labels=Portfolios, values=Demand, pull=[0, 0.3, 0, 0])])

app.layout = html.Div(children=[
    # All elements from the top of the page

    html.Div([
        html.H1(children='Gold Dataset'),
        html.H4(children=about_dataset),
        html.H2(children='Rank wise Gold Consumption per Quarter'),
        html.Div(children='''

        '''),

        dcc.Graph(
            id='graph1',
            figure=fig1
        ),
    ]),

    html.Div(children=[

        html.H2(children='Gold Reserves Region wise along with economic group'),
        dcc.Graph(
            id='graph2',
            figure=fig2
        )
    ]),

    html.Div([
            html.H2(children='Gold Reserves 2019 vs 2021 Region-wise'),
            html.Div(children='''
    
         '''),

            dcc.Graph(
                id='graph3',
                figure=fig3
            ),

        ]),

    html.Div([
        html.H2(children='Gold Reserves 2019 vs 2021 Economic condition-wise'),
        html.Div(children='''

         '''),

        dcc.Graph(
            id='graph4',
            figure=fig4
        ),

    ]),
    # # New Div for all elements in the new 'row' of the page

    html.Div([
        html.H2(children='Tree Map Exposure of Gold Reserves'),
        html.Div(children='''

   '''),
        dcc.Dropdown(
            Gold1921["YearEnd"].unique(),
            'Select the year by Drop Down',
            id='YearEnd'
        ),

        dcc.Graph(
            id='graph5'

        ),
        ]),

   html.Div([
       html.H2(children='Tree Map Exposure of Gold Reserves wrt Economic Condition'),
       html.Div(children='''

       '''),

        dcc.Graph(
            id='graph7',
            figure=fig7
        ),
      ]),

   html.Div([
        html.H2(children='Comparative study of Jewelery for Country'),
        html.Div(children='''

   '''),
        dcc.Dropdown(
            Jwellery1021.columns[1:].unique(),
            id='Year'
        ),

        dcc.Graph(
            id='graph8'
        ),

    ]),

   html.Div([
       html.H2(children='Comparative study of Jewelery for Region'),
       html.Div(children='''

       '''),
       dcc.Dropdown(
           Jwellery1021.columns[2:].unique(),
           id='Year1'
       ),
       dcc.Graph(
           id='graph9',
            #figure=fig8
       ),

   ]),

    html.Div([
        html.H2(children='Distribution of Gold reserves in the World'),
        html.Div(children='''

      '''),

        dcc.Graph(
            id='graph11',
            figure=fig11
        ),

    ]),

    html.Div([
            html.H2(children='Significance in Technology'),
            html.Div(children='''

        '''),

            dcc.Graph(
                id='graph10',
                figure=fig10
            ),

        ]),
])

@app.callback(
    Output(component_id='graph5',component_property='figure'),
    Input(component_id='YearEnd',component_property='value')
)

def update_graph(YearEnd):
    if type(YearEnd)==type(None):
        YearEnd=2019

    G1921=Gold1921[Gold1921["YearEnd"]==YearEnd]
    fig9 = px.treemap(G1921, path=[px.Constant("world"), 'Region','Country'], values='Total Reserves',
                      color='Gold Reserves Tonnes', hover_data=['Gold Reserves Tonnes'],
                      color_continuous_scale='RdBu'
                      )
    fig9.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig9

@app.callback(
    Output(component_id='graph8',component_property='figure'),
    Input(component_id='Year',component_property='value')
)


def update_bubblegraph(Year):
    if(type(Year)!=type(None)):
        fig9=px.scatter(Jwellery1021,y="Country", x=int(Year),size=int(Year), color="Country",
                        hover_name="Country",color_continuous_scale='RdBu', log_x=True,size_max=60)
    else:
        fig9 = px.scatter(Jwellery1021,y="Country", x=2010, size=2010,
                          color="Country",
                          hover_name="Country",color_continuous_scale='RdBu', log_x=True,size_max=60)
    return fig9


@app.callback(
    Output(component_id='graph9',component_property='figure'),
    Input(component_id='Year1',component_property='value')
)
def update_bubblegraph(Year):
    if(type(Year)!=type(None)):
        fig7=px.scatter(Jwellery1021,y="Region", x=int(Year),size=int(Year), color="Region",
                        hover_name="Region",color_continuous_scale='RdBu', log_x=True,size_max=60)
    else:
        fig7 = px.scatter(Jwellery1021,y="Region", x=2010, size=2010,
                          color="Region",
                          hover_name="Country",color_continuous_scale='RdBu', log_x=True,size_max=60)
    return fig7


if __name__ == '__main__':
    app.run_server(debug=True)

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import urllib.request, json

path_datasets = 'https://raw.githubusercontent.com/marcoelumba/on-energy-consumption/master/datasets/'

with urllib.request.urlopen(path_datasets + 'countries.geojson') as url:
    data_geo = json.loads(url.read().decode())

df = pd.read_csv(path_datasets + 'global-energy-use.csv')
df_e = pd.read_csv(path_datasets + 'fossilfueldata.csv')
df_c = pd.read_csv(path_datasets + 'per-capita-energy-use.csv')

# Calling country name
for feature in data_geo['features']:
    feature['id'] = feature['properties']['ADMIN']

continent_list = set(df.Continent)
continent_list.update(continent_list, ['World'])
Country = set(df.Country)

fig_sunburst = px.sunburst(df_e[(df_e["Category"].str.contains("Consumption")) & (df_e["Usage"] > 0.0) & (df_e["Year"] == 2020)],
                  path=['FossilType', 'Continent', 'Country'],
                  values='Usage')
fig_sunburst = fig_sunburst.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),'font_color':'#363535'})
fig_line = px.line(df_c, x="Year", y="Energy per capita (kWh)", color='Entity')
fig_line = fig_line.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),'font_color':'#363535',
                                   'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})
app = Dash(__name__)

app.layout = html.Div([

    html.H1("On energy consumption"),
    html.Div([
        #TOP
        html.Div([
            html.Label('Global Energy Consumption', style={'font-size': 'medium'}),
            html.Div([
                        html.Label('Continent', style={'font-size': 'medium'}),
                        dcc.Dropdown(
                            id="continent-dropdown",
                            options=[{'label': i, 'value': i} for i in sorted(continent_list)],
                            value='World'
                        )
                    ], style={'position': 'absolute', 'width': '10%', 'right': '5%', 'font-size':'12px'}
                        , className='continent_dropdown'),
            html.Br(), html.Br(),html.Br(),html.Br(),
            html.Div([
                        dcc.Graph(id="global-map"),
                    ], style={'position': 'absolute', 'width': '80%', 'right': '5%', 'font-size':'12px'},  className='map')

        ], style={'position': 'relative', 'width': '100%', 'top': '0px'}, className='top_div'),
        #END OF TOP

        html.Br(),
        #MID
        html.Div([
            html.Div([
                        dcc.Dropdown(
                            id="country-dropdown",
                            options=[{'label': i, 'value': i} for i in sorted(Country)],
                            value='Portugal'
                        )
                    ], style={'position': 'relative', 'width': '10%', 'left': '40%', 'font-size':'12px'}
                        , className='country_dropdown'),
            html.Div([
                    dcc.Graph(id="fossil_bar_chart"),
            ], style={'position': 'absolute', 'width': '55%', 'height': '500', 'left': '1%' , 'opacity':'100%'}, className='bar_chart'),
            html.Div([
                    dcc.Graph(figure=fig_sunburst),
            ], style={'position': 'absolute','width': '40%', 'height': '200', 'right': '1%', 'opacity':'100%'}, className='sun_burst')
        ], style={'position': 'absolute', 'width': '100%', 'height': '520', 'marginTop': 510} , className='mid_div'),
        #END OF MID

        html.Br(),
        #BOT
        html.Div([
            html.Div([
                    dcc.Graph(figure=fig_line),
            ], style={'position': 'relative', 'width': '80%', 'height': '500', 'bottom': '1%', 'opacity':'100%'}, className='line_chart_div')
        ], style={'position': 'relative', 'width': '100%', 'left': '0%', 'bottom': '0px', 'marginTop': 1000}, className='bot_div')
        #BOT OF MID

    ], style={'position': 'absolute', 'width': '100%',})
], style={'textAlign': 'center'})


@app.callback(
    Output("global-map", "figure"),
    Input("continent-dropdown", "value")
)
def world_map(continent):
    if continent == 'World':
        df_map = df
    else:
        df_map = df[df.Continent == continent]

    fig = px.choropleth(
        df_map,
        #geojson= data_geo,
        locations='iso_alpha',
        color='TotalConsumption',
        hover_name='Country',
        # color_continuous_midpoint=df.TotalConsumption.mean(),
        color_continuous_scale="OrRd",
        animation_frame='Year',
        featureidkey="properties.ISO_A3",
        height=500,
        width=1300)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_layout({'margin': dict(t=0, l=0, r=0, b=10), 'font_color': '#363535'})
    return fig

@app.callback(
    Output("fossil_bar_chart", "figure"),
    Input("country-dropdown", "value")
)
def stackedbar(country):
    fig = px.bar(df_e[(df_e["Category"].str.contains("Consumption")) & (df_e["Country"] == country) & (df_e["Usage"] > 0.0)],
                     x="Year",
                     y="Usage",
                     color="Category",
                     title="Usage per fossil fuel")
    fig.update_layout(legend=dict( orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1))
    fig.update_layout({'margin': dict(t=0, l=0, r=0, b=10), 'font_color': '#363535' ,
                                   'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})
    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

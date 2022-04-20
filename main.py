from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from urllib.request import urlopen
import urllib.request, json

path_datasets = 'https://raw.githubusercontent.com/marcoelumba/on-energy-consumption/master/datasets/'

# Data Connections
df = pd.read_csv(path_datasets + 'global-energy-usage.csv')
df_e = pd.read_csv(path_datasets + 'fossilfueldata.csv')
df_c = pd.read_csv(path_datasets + 'per-capita-energy-use.csv')
df_x = pd.read_csv(path_datasets + 'annual-change-fossil-fuels.csv')

# Filter lists
continent_list = np.concatenate((df.Continent.unique(), 'World'), axis=None)
Country = df.Country.unique()


fig_sunburst = px.sunburst(df_e[(df_e["Category"].str.contains("Consumption")) & (df_e["Usage"] > 0.0) & (df_e["Year"] == 2020)],
                  path=['FossilType', 'Continent', 'Country'],
                  title="Share of fossil fuel usage per continent in 2020<br><sup>Share of consumption is measured in exajoules and grouped per fossil fuel type then continent</sup>",
                  values='Usage', color_discrete_map={'Oil Consumption': 'rgb(99, 110, 250)',
                                     'Gas Consumption': 'rgb(0, 204, 150)',
                                     'Coal Consumption': 'rgb(239, 85, 59)'})
fig_sunburst = fig_sunburst.update_layout({'margin': dict(t=60, l=0, r=0, b=0),'font_color':'#363535',
                                           'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})


app = Dash(__name__)

app.layout = html.Div([

    html.H1("Global Fossil Fuel Consumption (2020)", style={'font-family':'Arial, Helvetica, sans-serif'}),
    html.P("Source: Statistical Review of World Energy BP (This dashboard project is presented by: Marco E. [m20210982])", style={'font-family':'Arial, Helvetica, sans-serif', 'font-size': '10px', 'color' : '#989898'}),
    html.Div([
        #TOP
        html.Div([

            html.Div([
                html.H1('80%',style={'margin': dict(t=0, l=0, r=0, b=0), 'font_color': '#363535', 'text-align': 'right'}),
                html.P('Global Energy source is from Fossil Fuel', style={'margin': dict(t=0, l=0, r=0, b=0), 'font_color': '#363535', 'text-align': 'right' , 'font-size': '15px'}),
                html.H1('-5.57%', style={'margin': dict(t=0, l=0, r=0, b=0), 'font_color': '#363535', 'text-align': 'right'}),
                html.P("Wolrd consumption change in 2020", style={'margin': dict(t=0, l=0, r=0, b=0), 'font_color': '#363535', 'text-align': 'right' , 'font-size': '15px'}),
                html.H2('-2.08%', style={'margin': dict(t=0, l=0, r=0, b=0), 'color': '#4CBB17', 'text-align': 'right'}),
                html.P("Wolrd consumption change for Gas in 2020", style={'margin': dict(t=0, l=0, r=0, b=0), 'font_color': 'rgb(0, 204, 150)', 'text-align': 'right' , 'font-size': '15px'}),
                html.H2('-3.94%', style={'margin': dict(t=0, l=0, r=0, b=0), 'color': '#EC5800', 'text-align': 'right'}),
                html.P("Wolrd consumption change for Coal in 2020", style={'margin': dict(t=0, l=0, r=0, b=0), 'font_color': 'rgb(239, 85, 59)', 'text-align': 'right', 'font-size': '15px'}),
                html.H2('-4.66%', style={'margin': dict(t=0, l=0, r=0, b=0), 'color': '#4169E1', 'text-align': 'right'}),
                html.P("Wolrd consumption change for Oil in 2020", style={'margin': dict(t=0, l=0, r=0, b=0), 'font_color': '#363535', 'text-align': 'right', 'font-size': '15px'})
            ], style={'position': 'relative', 'width': '20%', 'top': '0px', 'float': 'left', 'font-family':'Arial, Helvetica, sans-serif'}, className='top_left'),


            html.Div([
                        dcc.Graph(id="global-map"),
                    ], style={'position': 'absolute', 'right': '2%', 'font-size':'12px', 'float': 'right',
                              'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)', 'opacity':'100%'},
                className='map'),


            html.Div([

                dcc.Dropdown(
                    id="continent-dropdown",
                    options=[{'label': i, 'value': i} for i in sorted(continent_list)],
                    value='World'
                )
            ], style={'position': 'relative', 'width': '10%', 'right': '10%', 'font-size': '12px', 'float': 'right',
                      'opacity': '100%'} , className='continent_dropdown'),
        ], style={'position': 'relative', 'width': '100%', 'top': '0px'}, className='top_div'),
        #END OF TOP

        html.Br(),
        #MID
        html.Div([
            html.Div([
                html.Div([
                        dcc.Graph(id="fossil_bar_chart"),
                ], style={'position': 'absolute', 'width': '95%', 'height': '500', 'left': '1%' ,
                          'opacity':'100%'}, className='bar_chart'),
                html.Br(),html.Br(),
                html.Div([
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{'label': i, 'value': i} for i in sorted(Country)],
                    value='Portugal', searchable=True
                ) ], style={'position': 'relative', 'width': '20%', 'left': '73%', 'font-size': '12px', 'opacity': '100%'}
                    , className='country_dropdown'),
            ], style={'position': 'relative', 'width': '60%', 'left': '0%', 'font-size': '12px', 'opacity': '100%' ,'float': 'left'}
                    , className='mid_left'),

            html.Div([
                    dcc.Graph(figure=fig_sunburst),
            ], style={'position': 'relative','width': '40%',
                      'right': '1%', 'opacity':'100%' ,'float': 'right'}, className='sun_burst')

        ], style={'position': 'absolute', 'width': '100%', 'height': '520', 'marginTop': 520,
                  'font-family':'Arial, Helvetica, sans-serif'}, className='mid_div'),
        #END OF MID
        html.Div([
                    dcc.ConfirmDialog(id='line-alert',
                                      message="Line Chart: Country selected should  not be greater then 5. \n Please remove the 6th and + country in the list."),
                    dcc.ConfirmDialog(id='bar-alert',
                                      message="Bar Chart: Country selected should  not be greater then 5. \n Please remove the 6th and + country in the list.")
                ]),
        #BOT
        html.Div([
            # BOTTOM LEFT
            html.Div([
                # Left Top
                html.Div([
                        html.Label(['Please select max 5 countries:'], style={'font-weight': 'bold', "text-align": "center", 'float': 'left'}}),
                        dcc.Dropdown(
                                    id="multi-dropdown",
                                    options=[{'label': i, 'value': i} for i in df_c.Country.unique()],
                                    value=['Portugal','Singapore','China','India','United States'],
                                    multi=True
                                )
                            ], style={'position': 'relative', 'width': '50%', 'bottom': '1%', 'left': '60%', 
                                       'font-size':'12px'}
                                , className='country_multi_dropdown'),
                # Left Bottom
                html.Br(),
                html.Div([
                        dcc.Graph(id='line-chart'),
                        ], style={'position': 'relative', 'width': '100%','height': '400', 'float': 'left',
                                'left': '2%', 'bottom': '1%', 'opacity':'100%'}, className='line_chart_div')
            ], style={'position': 'relative', 'width': '55%', 'height': '400', 'float': 'left' , 'opacity':'100%', 'font-family':'Arial, Helvetica, sans-serif'}, className='left-div'),
            # BOTTOM Right
            html.Div([
                # Right Top
                html.Div([
                       html.Label(['Please select max 5 countries:'], style={'font-weight': 'bold', "text-align": "left"}),
                        dcc.Dropdown(
                                        id="bmulti-dropdown",
                                        options=[{'label': i, 'value': i} for i in df_x.Country.unique()],
                                        value=['Portugal','Singapore','China','India','United States'],
                                        multi=True, searchable=True
                                    )
                                ], style={'position': 'relative', 'width': '60%', 'bottom': '1%',
                                          'right': '8%', 'font-size':'12px'}
                                    , className='country_bmulti_dropdown'),
                # Right Bottom
                html.Br(),
                html.Div([
                    dcc.Graph(id='hbar-chart'),
                            ], style={'position': 'relative',  'height': '400', 'float': 'right',
                                        'right': '5%', 'bottom': '1%', 'opacity': '100%'}, className='hbar_chart_div')

                ], style={'position': 'relative', 'height': '400', 'float': 'right', 'width': '45%',
                          'font-family':'Arial, Helvetica, sans-serif'}, className='bright-div')
        ], style={'position': 'relative', 'width': '100%',
                  'left': '0%', 'marginTop': 1010},
                    className='bot_div')
        #BOT OF MID
    ], style={'position': 'absolute', 'width': '100%'}),
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
        locations='iso_alpha',
        color='Usage',
        hover_name='Country',
        color_continuous_scale="YlOrRd",
        animation_frame='Year',
        featureidkey="properties.ISO_A3",
        projection="equirectangular",
        height=500,
        width=1300)
    fig.update_layout(legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="right", x=3)
                      , title_text='World Fossil Fuel Usage measured in Exajoules <br><sup>Fossil fuel consumption per year from coal, oil and gas per country</sup>',
                      coloraxis_colorbar=dict(
                          title="Consumption",
                          thicknessmode="pixels",
                          lenmode="pixels",
                          yanchor="top", y=1,
                          ticks="outside",
                          tickvals=[0, 30, 80, 130],
                          ticktext=["Low", "Low Medium", "High Medium", "High"])
                      )
    fig.update_layout({'margin': dict(t=50, l=0, r=0, b=10), 'font_color': '#363535'})
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
                     labels={
                         "Usage": "Energy usage (Exajoules)",
                         "Year": "Year (Recorder year)",
                         "Category": "Fossil Type:"
                     },
                    title='Country level energy consumption measured in Exajoules <br><sup>Consumption broken down by fossil fuel (coal, oil and gas) over time</sup>',
                    color_discrete_map={'Oil Consumption': 'rgb(99, 110, 250)',
                                     'Gas Consumption': 'rgb(0, 204, 150)',
                                     'Coal Consumption': 'rgb(239, 85, 59)'}
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.2, xanchor="right",x=1) , title_font_family="Arial")
    fig.update_layout({'margin': dict(t=20, l=0, r=0, b=10), 'font_color': '#363535' ,
                                   'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})
    return fig

@app.callback(
    [Output("line-chart", "figure"),
     Output("line-alert", "displayed")],
    Input("multi-dropdown", "value")
)
def linechart(country):
    if len(country) <=5:
        fig = px.line(df_c[df_c.Country.isin(country)],
                      x="Year",
                      y="Energy per capita (kWh)",
                      color='Country',
                      markers=True,
                      title='Energy consumption per capita<br><sup>All types of energy consumption per capita is measured as the average consumption of energy</sup>')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.15, xanchor="right", x=1))
        fig = fig.update_layout({'margin': dict(t=80, l=0, r=0, b=10), 'font_color': '#363535',
                                 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})
        return fig, False
    else:
        fig = px.line(df_c[df_c.Country.isin(country[0:5])],
                      x="Year",
                      y="Energy per capita (kWh)",
                      color='Country',
                      markers=True,
                      title='Fossil fuel consumption per capita<br><sup>Fossil fuel consumption per capita is measured as the average consumption of energy from coal, oil and gas per person</sup>')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.15, xanchor="right", x=1, title='Country'))
        fig.update_layout({'margin': dict(t=50, l=0, r=0, b=10), 'font_color': '#363535',
                                 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})
        return fig, True

@app.callback(
    [Output("hbar-chart", "figure"),
     Output("bar-alert", "displayed")],
    Input("bmulti-dropdown", "value")
)
def hbarchart(country):
    if len(country) <=5:
        fig = px.bar(df_x[df_x.Country.isin(country)],
                     x="Consumption Change (TW)",
                     y="Country",
                      hover_name='Country',
                      color='Country',
                      animation_frame='Year',
                      title='Fossil fuel consumption change<br><sup>Fossil fuel consumption change is measured as the average consumption in terawatts</sup>')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.15, xanchor="right", x=1))
        fig = fig.update_layout({'margin': dict(t=40, l=0, r=0, b=10), 'font_color': '#363535',
                                 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})
        return fig, False
    else:
        fig = px.bar(df_x[df_x.Country.isin(country[0:5])],
                     x="Consumption Change (TW)",
                     y="Country",
                      hover_name='Country',
                      color='Country',
                      animation_frame='Year',
                      title='Fossil fuel consumption change<br><sup>Fossil fuel consumption change is measured as the average consumption in terawatts</sup>')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.15, xanchor="right", x=1))
        fig = fig.update_layout({'margin': dict(t=40, l=0, r=0, b=10), 'font_color': '#363535',
                                 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'})
        return fig, True

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

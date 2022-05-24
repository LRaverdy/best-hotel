import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

weather = pd.read_csv("city_weather.csv")
hotels = pd.read_csv("kayak.csv")


# Hide plotly toolbar options
config = {'displaylogo' : False,
          'modeBarButtonsToRemove': [
            'zoom2d',
            'pan2d',
            'select2d',
            'lasso2d',
            'zoomIn2d',
            'zoomOut2d',
            'toImage',
            'resetScale2d'
          ]}


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1 , maximum-scale=1.9, minimum-scale=.5'}])

server = app.server

########################################################
###################### App Layout ######################
########################################################


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([

            dcc.Markdown("*Find the best hotels in your city*",
                         className="lead",
                         style={"font-size": 30,
                                "textAlign": "center",
                                "color": "white"})

        ], xl=6, lg=6, xs=12, align='center')
    ], justify="center", style={"background-color": "black"}),

    dbc.Row([
        dbc.Col([

            dcc.RadioItems(
                options=[
                    {'label': 'Morning', 'value': 'morning_temp'},
                    {'label': 'Day', 'value': 'day_temp'},
                    {'label': 'Evening', 'value': 'evening_temp'},
                    {'label': 'Night', 'value': 'night_temp'}
                ],
               value='day_temp',
                id="weather_radio",
                labelStyle={  # Different padding for the checklist elements
                          'display': 'inline-block',
                          'paddingRight': 10,
                          'paddingLeft': 10,
                          'paddingBottom': 10,
                      }
                #={"textAlign": "center"}
            ),

            dcc.Graph(id="weather_map",
                      figure={},
                      style={
                          "height": "600px",
                          "width": "100%"
                      })

        ], xl=6, lg=6, xs=12, style={
            "background-color": "lightgrey",
            "paddingTop": 25,
            "paddingBottom": 30}),

        dbc.Col([

            dcc.Dropdown(
                        id="slct_city",
                        options=[{
                            "label": f"{x}",
                            "value": x} for x in sorted(hotels['city'].unique())],
                        multi=False,
                        value="Cassis",
                        style={
                            'width': "50%",
                            'color': 'black',
                            'font-size':'90%'
                        }),

            dcc.Graph(id="hotel_map",
                      figure={},
                      style={
                          "height": "600px",
                          "width": "100%"
                      })


        ], xl=6, lg=6, xs=12, style={
            "background-color": "lightgrey",
            "paddingTop": 25,
            "paddingBottom": 30})

    ], justify="center", style={"background-color": "lightgrey,"})

], fluid=True, style={"background-color": "lightgrey"})





########################################################
###################### CallBacks #######################
########################################################

@app.callback(
    Output("weather_map", "figure"),
    Input("weather_radio", "value")
)

def update_map(temp):


    if temp == "morning_temp":
        title = "Morning temperature"

    elif temp == "day_temp":
        title = "Day temperature"

    elif temp == "evening_temp":
        title = "Evening temperature"

    else:
        title = "Night temperature"


    mapbox_access_token = 'pk.eyJ1IjoibGV3aXN3ZXJuZWNrIiwiYSI6ImNsMnMzYnA1OTA5dXgza25yazhhajh3NGsifQ.Z3CrpQqY0Xj_ZH3spiAiYQ'

    # Defaut color_scale before function
    color_scale = None

    # Plotting map
    fig = px.scatter_mapbox(
        weather,
        lat=weather['latitude'].astype(float),
        lon=weather['longitude'].astype(float),
        # text=[str(i) for i in df["day_temp"]],
        size=temp,
        hover_name='city',
        hover_data=weather[[temp, "min_temp", "max_temp"]],
        color=temp,
        zoom=4,
        # opacity = 0.7,
        color_continuous_scale=["darkblue",
                                "blue",
                                "lightblue",
                                "yellow",
                                "yellow",
                                "red"]  # Applying our color scale function
    )

    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=50, b=50, l=0, r=0),
        title=title,
        title_x=.5,
        #title_font_size=14,
        mapbox_style='open-street-map',
        mapbox=dict(accesstoken=mapbox_access_token)
    )

    fig.update_traces(marker_size=15, selector=dict(type='scattermapbox'))

    return fig


@app.callback(
    Output("hotel_map", "figure"),
    Input("slct_city", "value")
)


def update_map(city):
    mapbox_access_token = 'pk.eyJ1IjoibGV3aXN3ZXJuZWNrIiwiYSI6ImNsMnMzYnA1OTA5dXgza25yazhhajh3NGsifQ.Z3CrpQqY0Xj_ZH3spiAiYQ'

    # Plotting map
    fig = px.scatter_mapbox(
        hotels[hotels["city"] == city],
        lat='latitude',
        lon='longitude',
        hover_name='hotels',
        hover_data=None,
        color='score',
        zoom=13,
        color_continuous_scale=['darkblue', 'blue', 'red', 'red']
    )

    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=50, b=50, l=0, r=0),
        title=f"Best hotels in {city}",
        title_x=.5,
        #title_font_size=14,
        mapbox_style='open-street-map',
        mapbox=dict(accesstoken=mapbox_access_token)
    )

    fig.update_traces(marker_size=15, selector=dict(type='scattermapbox'))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
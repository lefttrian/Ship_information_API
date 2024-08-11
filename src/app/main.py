from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from folium import Map, plugins
import geopandas

from .database import DatabaseConnector

from .data import load_weather_data

description = """
Xomnia assessment API.
"""

tags_metadata = [
    {
        "name": "ships",
        "description": "For how many ships do we have available data?",
    },
    {
        "name": "hourly_speed",
        "description": "Avg speed for all available ships for each hour of the date 2019-02-13.",
    },
    {
        "name": "min_max_speed",
        "description": "Max & min wind speed for every available day for ship ”st-1a2090” only",
    },
    {
        "name": "map",
        "description": "In order for the visualisation to work, you need to use the url http://localhost:8080/map."
                       "A way to visualize full weather conditions (example fields: general description, temperature, "
                       "wind speed) across route of the ship ”st-1a2090” for date 2019-02-13. In case of time "
                       "pressure, the application could simply return the requested data instead of a visualization.",
    },
    {
        "name": "full_data",
        "description": "Our colleagues from BI would like to collect history of the data during our fleet’s travels "
                       "combined with the weather conditions so that they can perform analysis on the impact of "
                       "weather to our operations, therefore the application should persist the data in any kind of "
                       "database system of your choice."
        ,
    }
]

app = FastAPI(openapi_tags=tags_metadata,description=description)


@app.get('/')
async def read_root():
    return {"Message": "Xomnia assessment API"}


@app.get('/number_of_ships', tags=['ships'])
async def read():
    db = DatabaseConnector()
    return {f"Number of ships with data: {db.get_distinct_count_of_ships('device_id')}"}


@app.get('/avg_hourly_speed_for_date', tags=['hourly_speed'])
async def read():
    db = DatabaseConnector()
    df = db.get_avg_speed_per_hour()
    return Response(df.to_json(orient="records"), media_type="application/json")


@app.get('/ship_min_max_speed_per_day', tags=['min_max_speed'])
async def read():
    db = DatabaseConnector()
    df = db.get_ship_min_max_speed_per_day()
    return Response(df.to_json(orient="records"), media_type="application/json")


@app.get('/full_data', tags=['full_data'])
async def read():
    db = DatabaseConnector()
    df = db.get_data_with_weather()
    return Response(df.to_json(orient="records"), media_type="application/json")


@app.get("/map", response_class=HTMLResponse, tags=['map'])
async def root():
    m = Map(location=[15, 30], tiles="Cartodb dark_matter", zoom_start=2)
    weather = load_weather_data()
    geometry = geopandas.points_from_xy(weather.lon, weather.lat)
    geo_df = geopandas.GeoDataFrame(
        weather[["wind_spd"]], geometry=geometry
    )
    heat_data = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry]
    plugins.HeatMap(heat_data).add_to(m)
    return m.get_root().render()

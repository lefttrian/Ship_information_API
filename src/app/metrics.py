import pandas as pd
from .database import DatabaseConnector
from .data import load_weather_data
'''
Calculations for the metrics. 
Two of the calculations persist the results in the sqlite db.
'''

def number_of_ships() -> int:
    db = DatabaseConnector()
    return db.get_distinct_count_of_ships('device_id')


def avg_hourly_speed_for_date(data, date) :
    filtered_data = data[(data['datetime'].dt.date == pd.to_datetime(date).date())]
    avg_speed_per_hour = filtered_data.groupby([filtered_data['datetime'].dt.hour, 'device_id'])[
        'spd_over_grnd'].mean().reset_index()
    db = DatabaseConnector()
    db.save_dataframe(avg_speed_per_hour, 'avg_speed_per_hour')
    return


def ship_min_max_speed_per_day(data, ship) :
    filtered_data = data[data['device_id'] == ship]
    weather = load_weather_data()
    df_with_weather = pd.merge(filtered_data, weather, left_on=['lat', 'lon'], right_on=['lat', 'lon'])
    wind_spd_stats = df_with_weather.groupby(df_with_weather['datetime_x'].dt.date)['wind_spd'].agg(['max', 'min']).reset_index()
    df_with_weather['sources']=df_with_weather['sources'].astype(str)
    db = DatabaseConnector()
    db.save_dataframe(df_with_weather,'df_with_weather')
    db.save_dataframe(wind_spd_stats,'wind_spd_stats')
    return

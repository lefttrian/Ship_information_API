import numpy as np
import pandas as p
from .database import DatabaseConnector
import os
'''
Contains data processing - cleaning operations
Each process persists the data in a sqlite db
'''

def clean_data(file):
    column_names = {0: 'status', 1: 'lat', 2: 'lat_dir', 3: 'lon', 4: 'lon_dir', 5: 'spd_over_grnd', 6: 'true_course',
                    7: 'datestamp', 8: 'mag_variation', 9: 'mag_var_dir'}
    df = p.read_csv(file)
    df_raw_message = df['raw_message'].str.split(',', expand=True)
    df_raw_message = df_raw_message.rename(columns=column_names)
    df_raw_message = df_raw_message.apply(lambda x: x.str.replace(r'[^a-zA-Z0-9.]', '', regex=True))
    df.drop('raw_message', axis=1, inplace=True)
    df['datetime'] = p.to_datetime(df['datetime'], unit='s')
    cleaned_df = p.concat([df, df_raw_message], axis=1)
    cleaned_df = cleaned_df.astype({"spd_over_grnd": float, "lat": float, "lon": float})
    db = DatabaseConnector()
    db.save_dataframe(cleaned_df,'data')
    return cleaned_df


def load_weather_data() -> p.DataFrame:
    filename = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', 'data','weather_data.json'))
    weather = p.read_json(filename)
    weather['index'] = np.arange(weather.shape[0])
    weather_data = p.json_normalize(weather['data'])
    weather_data['index'] = np.arange(weather_data.shape[0])
    z = weather_data.melt(id_vars=['index'], var_name='record', value_name='data')
    z = p.concat([z, p.json_normalize(z['data'])], axis=1)
    weather.drop('data', axis=1, inplace=True)
    z.drop('data', axis=1, inplace=True)
    weather_data_final = p.merge(weather, z, left_on='index', right_on='index')
    return weather_data_final

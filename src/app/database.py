import sqlite3
import pandas as pd

'''
contains necessary class to handle sqlite db operations
'''

class DatabaseConnector:
    def __init__(self):
        self.conn = sqlite3.connect('xomnia.sqlite')

    def save_dataframe(self, df: pd.DataFrame, name: str):
        df.to_sql(name, self.conn, if_exists='replace', index=False)
        return f"Table {name} created."

    def get_distinct_count_of_ships(self, column):
        cur = self.conn.cursor()
        cur.execute(f'select count(distinct {column}) from data')
        result = cur.fetchone()
        return result[0]

    def get_avg_speed_per_hour(self) -> pd.DataFrame:
        df = pd.read_sql('select * from avg_speed_per_hour', self.conn)
        return df

    def get_ship_min_max_speed_per_day(self) -> pd.DataFrame:
        df = pd.read_sql('select * from wind_spd_stats', self.conn)
        return df

    def get_data_with_weather(self) -> pd.DataFrame:
        df = pd.read_sql('select * from df_with_weather', self.conn)
        return df

    def __del__(self):
        self.conn.close()

from .data import clean_data
from .metrics import avg_hourly_speed_for_date, ship_min_max_speed_per_day
import os
'''
Runs the subprocesses in the proper order
'''
def process():
    filename = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', 'data','raw_messages.csv'))
    df=clean_data(filename)
    avg_hourly_speed_for_date(df,'2019-02-13')
    ship_min_max_speed_per_day(df,'st-1a2090')
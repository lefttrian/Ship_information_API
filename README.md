# Xomnia assessment

## Purpose:
Cleans the original data, calculates metrics, exposes the results via an API and persists the data in a sqlite db (to keep things small and cheap).

A running version can be found at https://whispering-depths-10973-2ebc17a4b6d0.herokuapp.com/docs.

## Endpoints:

- /number_of_ships
  - For how many ships do we have available data?

- /avg_hourly_speed_for_date
  - Avg speed for all available ships for each hour of the date 2019-02-13.

- /ship_min_max_speed_per_day
  - Max & min wind speed for every available day for ship ”st-1a2090” only

- /full_data
  - Our colleagues from BI would like to collect history of the data during our fleet’s travels combined with the weather conditions so that they can perform analysis on the impact of weather to our operations, therefore the application should persist the data in any kind of database system of your choice.

- /map
  - way to visualize full weather conditions (example fields: general description, temperature, wind speed) across route of the ship ”st-1a2090” for date 2019-02-13. In case of time pressure, the application could simply return the requested data instead of a visualization.

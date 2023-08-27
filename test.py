from python_snowflake import PythonSnowflake
import plotly.express as px
import pandas as pd
from sql_utils import vaccine_query, european_latest

ps = PythonSnowflake()
conn = ps.create_connection()
df = ps.execute_sql(conn, european_latest())[0]

fig = px.choropleth(df, 
                    locationmode='country names',
                    locations = 'COUNTRY_REGION',
                    color = 'MOSTRECENTCASES',
                    scope = 'europe',
                    color_continuous_scale=[[0, 'rgb(255,212,212)'],
                      [0.05, 'rgb(253,183,183)'],
                      [0.1, 'rgb(252,152,152)'],
                      [0.20, 'rgb(249,120,120)'],
                      [1, 'rgb(255,0,0)']])


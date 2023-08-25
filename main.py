import snowflake.connector
import os
import pandas as pd
from snowflake.connector.secret_detector import SecretDetector
from python_snowflake import PythonSnowflake

ps = PythonSnowflake()
conn = ps.create_connection()

results = ps.execute_sql(conn, "SELECT * FROM WHO_DAILY_REPORT LIMIT 5 ")

print(results)


























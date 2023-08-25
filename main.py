from flask import Flask
import snowflake.connector
import os
import pandas as pd
from snowflake.connector.secret_detector import SecretDetector
from base import PythonBase

pb = PythonBase()
conn = pb.create_connection()
cur = conn.cursor()



# cur.execute_async("SELECT * FROM WHO_DAILY_REPORT LIMIT 5 ")
# query_id = cur.sfqid
# cur.get_results_from_sfqid(query_id)
# results = cur.fetch_pandas_all()
# print(f'{results}')
# print(type(results))






























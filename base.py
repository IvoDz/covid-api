import logging
import os
import sys
import snowflake.connector
from snowflake.connector.converter_null import SnowflakeNoConverterToPython
import pandas as pd


class PythonSnowflake:
    def __init__(self, p_log_file_name = 'logs.log'):
        file_name = p_log_file_name
        if file_name is None:
            file_name = '/tmp/snowflake_python_connector.log'

        logging.basicConfig(
            filename=file_name,
            level=logging.INFO)
        
        print("Welcome!")


    def create_connection(self):
        USER = os.getenv('user_snow')
        PASSWORD = os.getenv('pwd_snow')
        ACCOUNT = os.getenv('acc_snow')
        WAREHOUSE = os.getenv('warehouse_snow')
        DATABASE = os.getenv('database_snow')
        print("Connecting...")
        try:
            conn = snowflake.connector.connect(
            user=USER,
            password=PASSWORD,
            account=ACCOUNT,
            warehouse=WAREHOUSE,
            database=DATABASE,
            converter_class=SnowflakeNoConverterToPython
            )
            print(f"Success! Connected to DB {DATABASE}, using warehouse : {WAREHOUSE}")
        except snowflake.connector.errors.Error as e:
            print(f"Error: {e}")
        return conn


    def execute_sql(self, conn, query, to_df = True):
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetch_pandas_all() if to_df else cursor.fetchall()
            print(f"Query Successful!")
            return results
        except snowflake.connector.errors.Error as e:
            return f"Error while querying : {e}"




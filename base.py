import logging
import os
import sys
import snowflake.connector
from snowflake.connector.converter_null import SnowflakeNoConverterToPython


class PythonBase:
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


    def do_work(self, conn):
        print("Let's do some work!")


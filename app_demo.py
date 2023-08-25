import os
from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
from base import PythonSnowflake

# Initialize Flask app
app = Flask(__name__)
ps = PythonSnowflake()
conn = ps.create_connection()

# Route for the main page
@app.route('/', methods=['GET'])
def index();
    return render_template('index.html')


# df =  ps.execute_sql(conn, "SELECT * FROM WHO_DAILY_REPORT LIMIT 5 ")
# if not df.empty:
#     trace = go.Bar(x=df['COUNTRY_REGION'], y=df['CASES_TOTAL'])
#     data = [trace]
#     layout = go.Layout(title='Snowflake Data Visualization')
#     fig = go.Figure(data=data, layout=layout)
#     chart = fig.to_html(full_html=False)



if __name__ == '__main__':
    app.run(debug=True)
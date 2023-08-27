from flask import Flask, request, jsonify, render_template, session
from snowflake.connector.converter_null import SnowflakeNoConverterToPython
import pandas as pd
from python_snowflake import PythonSnowflake


app = Flask(__name__)
ps = PythonSnowflake()
conn = ps.create_connection()
app.secret_key = 'samplekey'

#### PARAMS to_df, query
@app.route('/execute-sql', methods=['GET', 'POST'])
def execute_sql():
    if request.method == 'GET':
        latest_query = session.get('latest_query', '')
        return render_template('query.html', latest_query=latest_query)

    
    # Handle POST request (execute SQL query)
    data = request.form  # Use request.form to access form data
    query = data.get('query')
    session['latest_query'] = query
    to_df = data.get('to_df', True)
    pretty = data.get('pretty', 0)
    resp = ps.execute_sql(conn, query, to_df)
    result, qid  = resp[0], resp[1]

    if isinstance(result, str):
        return jsonify({"error": result}), 500
    else:
        if pretty: 
            df_html = result.to_html(classes='table table-striped')
            return render_template('query_pretty.html', df_html=df_html, id = qid, query = query)
        else :
            return jsonify({"result": result.to_dict()}), 200
    

# 
#@app.route('/visualize', methods=['POST'])
#def generate_visualization():
    data = request.json
    # Extract relevant data from the request and use Plotly to generate visualizations
    # You can create various predefined visualization functions here.
    # Example: bar chart, line chart, pie chart, etc.

    # Return the visualization as JSON or an image file, depending on your needs.

    #return jsonify({"visualization": "your_visualization_data_or_path"}), 200


if __name__ == "__main__":
    app.run(debug=True)
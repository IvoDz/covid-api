from flask import Flask, request, jsonify, render_template, session, redirect
import pandas as pd
from python_snowflake import PythonSnowflake
from pymongo import MongoClient
from feedback import Feedback
from visuals import Visualizer

app = Flask(__name__)
ps = PythonSnowflake()
conn = ps.create_connection()
app.secret_key = 'samplekey'

client = MongoClient()
client = MongoClient("localhost", 27017)
db = client.covid
feedbacks = db["feedback"]

visualizer = Visualizer()

@app.route('/execute-sql', methods=['GET', 'POST'])
def execute_sql():
    if request.method == 'GET':
        latest_query = session.get('latest_query', '')
        return render_template('query.html', latest_query=latest_query)

    data = request.form
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
    

@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    # Generating json doc to insert
    feedback = request.form 
    user = feedback.get('name', 'Not specified')
    comment = feedback.get('comment', None)
    fav = feedback.get("favorite", False)

    fb = Feedback(user, comm = comment, favorite = fav)
    feedback_json = fb.get_feedback()

    try:
        feedbacks.insert_one(feedback_json)
        return redirect(request.referrer), 200

    except Exception as e:
        return redirect(request.referrer), 500


@app.route('/visualize/vaccines-total')
def visualize():
    pass


if __name__ == "__main__":
    app.run(debug=True)

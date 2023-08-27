from flask import Flask, request, jsonify, render_template, session, redirect
import pandas as pd
from python_snowflake import PythonSnowflake
from pymongo import MongoClient
from feedback import Feedback
from visuals import Visualizer
from flask_caching import Cache

# Configuring app, caching, connecting to MongoDB, connecting to snowflake
config = {
    "DEBUG": True,         
    "CACHE_TYPE": "SimpleCache",  
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
ps = PythonSnowflake()
conn = ps.create_connection()
app.secret_key = 'samplekey'
app.config.from_mapping(config)
cache = Cache(app)

client = MongoClient()
client = MongoClient("localhost", 27017)
db = client.covid
feedbacks = db["feedback"]

visualizer = Visualizer(conn)

# Route section - All routes and possible parameters are defined below

"""
/execute-sql
GET - returns renders HTML form for passing parameters and entering query
POST - parameters => to_df (bool, optional => default True), pretty (bool, optional)
queries snowflake database, returns result as (data, status_code)
"""
@app.route('/execute-sql', methods=['GET', 'POST'])
@cache.cached(timeout=30)
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
    
"""
/send_feedback
POST - parameters => user (str, required), timestamp (timestamp, required), 
comment (str, non-required), favorite (bool, non-required)
saves user entered feedback to database, redirects back
"""
@app.route('/send_feedback', methods=['POST'])
@cache.cached(timeout=50)
def send_feedback():
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
"""
/visualize/escalation/<c1>/<c2>/<c3>
GET - takes 3 countries (required) as parameters,
plots COVID-19 infection rates in 2020 as line chart
"""
@app.route('/visualize/escalation/<c1>/<c2>/<c3>', methods=['GET'])
@cache.cached(timeout=50)
def visualize_escalation(c1,c2,c3):
    c1 = c1.capitalize() if c1 else None
    c2 = c2.capitalize() if c2 else None
    c3 = c3.capitalize() if c3 else None

    if not all(isinstance(c, str) for c in [c1, c2, c3]):
        return redirect(request.referrer), 500

    fig = visualizer.plot_3_escalation(c1, c2, c3)
    plot_div = fig.to_html(full_html=False)
    return render_template('visualization.html', plot_div=plot_div)

"""
/visualize/vaccine_ratio/<c1>
GET - takes 1 country (required) as parameter,
plots pie chart with vaccinated/non-vaccinated
people ratio in country
"""
@app.route('/visualize/vaccine_ratio/<c1>', methods=['GET'])
@cache.cached(timeout=50)
def visualize_vaccines(c1):
    if not isinstance(c1, str):
        return redirect(request.referrer), 500

    fig = visualizer.plot_country_vaccine_ratio(c1)
    plot_div = fig.to_html(full_html=False)
    return render_template('visualization.html', plot_div=plot_div)

"""
/visualize/european_latest/<c1>/<c2>/<c3>
GET - takes no parameters,
plots map of Europe with color scheme
mapped to severity of latest known weekly cases
"""
@app.route('/visualize/european_latest', methods=['GET'])
@cache.cached(timeout=50)
def visualize_europe():
    fig = visualizer.european_latest_cases()
    plot_div = fig.to_html(full_html=False)
    return render_template('visualization.html', plot_div=plot_div)

"""
/visualize/expectancy_mortality
GET - takes no parameters, 
plots scatter plot depicting correlation between
life expectancy and COVID mortality in each country
"""
@app.route('/visualize/expectancy_mortality', methods=['GET'])
@cache.cached(timeout=50)
def mort_exp():
    fig = visualizer.scatter_exp_mort()
    plot_div = fig.to_html(full_html=False)
    return render_template('visualization.html', plot_div=plot_div)

"""
/visualize/happy_vac
GET - takes no parameters, 
plots scatter plot depicting correlation between
happiness score and COVID vaccination rates in each country
"""
@app.route('/visualize/happy_vac', methods=['GET'])
@cache.cached(timeout=50)
def happiness_vaccs():
    fig = visualizer.happy_vs_vaccinated()
    plot_div = fig.to_html(full_html=False)
    return render_template('visualization.html', plot_div=plot_div)


if __name__ == "__main__":
    app.run(debug=True)

// README.md
# covid_api
### Introduction
This API enables users to query Snowflake database and generate dynamic visualizations.  
### Key features
* Users can make custom SQL queries and retrieve results from Snowflake either as Pandas Dataframe or JSON
* Users can choose from 5 visualization types and access them via predefined endpoints 
* Feedback can be left about every resource (query result/visualizations)
### Installation Guide
* Clone this repository from [here](https://github.com/IvoDz/covid_api)
* Make sure you have active Snowflake account, save credentials as environmental variables.
* Make a new MongoDB database.
* Run pip install -r requirements.txt to install dependencies.
### Usage
* Navigate to project folder, run api.py file
* You have to see this message, then you can access API on port 5000
![image](https://github.com/IvoDz/covid_api/assets/97388815/bf8fa965-59ee-43ff-ab57-fe2e9999db98)
* You can access all endpoints on port 5000 by default.
* Use queries below to test functionality
### API Endpoints
| Request | Endpoint | Action |
| --- | --- | --- |
| GET | /execute-sql | To render html page with interactive form |
| POST | /execute-sql | To execute query in Snowflake and get result in desired format |
| POST | /send_feedback | Saves your comment to the DB |
| GET | /api/causes | To retrieve all causes on the platform
| GET | /visualize/vaccine_ratio/<country> | plots pie chart with vaccinated/non-vaccinated people ratio in country |
| GET | /visualize/european_latest | Shows interactive map of Europe with all recently available COVID cases |
| GET | /visualize/escalation/<c1>/<c2>/<c3> | Plots daily COVID cases in 2020 for 3 countries side by side |
| GET | /visualize/happy_vac | Plots scatter plot that shows relationship between happiness in the country and vaccination rate |
| GET | /visualize/expectancy_mortality | Plots scatter plot that shows relationship between life expectancy in the country and COVID mortality rate |

### Some examples with results
# visualize/vaccine_ratio/latvia 
![image](https://github.com/IvoDz/covid_api/assets/97388815/12ab9fec-b8e5-49f8-b4bc-f57df3efdf95)

# /visualize/happy_vac
![image](https://github.com/IvoDz/covid_api/assets/97388815/42484c8d-36d4-4200-9358-7ce0c5318770)

# visualize/european_latest
![image](https://github.com/IvoDz/covid_api/assets/97388815/55c757c1-59e3-409f-95d3-c77140657554)











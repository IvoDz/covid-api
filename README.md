### API Endpoints
| Request | Endpoint | Action |
| --- | --- | --- |
| GET | /execute-sql | To render html page with interactive form |
| POST | /execute-sql | To execute query in Snowflake and get result in desired format |
| POST | /send_feedback | Saves your comment to the DB |
| GET | /visualize/vaccine_ratio/_country_ | plots pie chart with vaccinated/non-vaccinated people ratio in country |
| GET | /visualize/european_latest | Shows interactive map of Europe with all recently available COVID cases |
| GET | /visualize/escalation/_c1_/_c2_/_c3_ | Plots daily COVID cases in 2020 for 3 countries side by side |
| GET | /visualize/happy_vac | Plots scatter plot that shows relationship between happiness in the country and vaccination rate |
| GET | /visualize/expectancy_mortality | Plots scatter plot that shows relationship between life expectancy in the country and COVID mortality rate |

### Some examples with results
# visualize/vaccine_ratio/latvia 
![image](https://github.com/IvoDz/covid_api/assets/97388815/12ab9fec-b8e5-49f8-b4bc-f57df3efdf95)

# /visualize/happy_vac
![image](https://github.com/IvoDz/covid_api/assets/97388815/42484c8d-36d4-4200-9358-7ce0c5318770)

# visualize/european_latest
![image](https://github.com/IvoDz/covid_api/assets/97388815/55c757c1-59e3-409f-95d3-c77140657554)











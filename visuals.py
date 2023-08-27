from python_snowflake import PythonSnowflake
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from sql_utils import vaccine_query, country_escalation, european_latest, life_exp, death_ratio, happy_df, countries_vacc

ps = PythonSnowflake()
"""
class Visualizer
Handles all visualization logic and chart generation with plotly
Currently supports 5 predefined yet flexible charts that have parameter support
Later on visible in visualization.html view
"""
class Visualizer:
    def __init__(self, conn):
        self.conn = conn

    # Plots COVID-19 infection rates in 2020 as line chart (3 countries side by side -- Baltics by default)
    def plot_3_escalation(self, country1="Latvia", country2="Lithuania", country3="Estonia"):
        df1 = ps.execute_sql(self.conn, country_escalation(country1))[0]
        df2 = ps.execute_sql(self.conn, country_escalation(country2))[0]
        df3 = ps.execute_sql(self.conn, country_escalation(country3))[0]

        fig = px.line(title=f'Escalation of Cases - {country1}, {country2}, {country3}')

        fig.add_trace(px.line(df1, x='DATE', y='CASES', title=country1).data[0])
        fig.add_trace(px.line(df2, x='DATE', y='CASES', title=country2).data[0])
        fig.add_trace(px.line(df3, x='DATE', y='CASES', title=country3).data[0])

        fig.update_layout(showlegend=True, title_x=0.5)

        return fig
    
    # plots pie chart with vaccinated/non-vaccinated people ratio in given country.
    def plot_country_vaccine_ratio(self, country):
        df = ps.execute_sql(self.conn, vaccine_query(country))[0]
        fig = px.pie(df, values=[df['PERC_VAC'].iloc[0], df['PERC_NOT_VAC'].iloc[0]], names=['Vaccinated', 'Not Vaccinated'],
                    color_discrete_map={'Vaccinated': 'green', 'Not Vaccinated': 'red'})

        fig.update_traces(textinfo='percent+label', pull=[0, 0.1], marker=dict(line=dict(color='#000000', width=1)))

        country = country.capitalize()
        fig.update_layout(title=f'Vaccination Status in {country}', showlegend=True, title_x=0.5)

        return fig
    
    # Plots map of Europe with color scheme mapped to severity of latest known weekly cases
    # where red - severe, white - no cases
    def european_latest_cases(self):
        df = ps.execute_sql(self.conn, european_latest())[0]

        fig = px.choropleth(df, 
                    locationmode='country names',
                    locations = 'COUNTRY_REGION',
                    color = 'MOSTRECENTCASES',
                    scope = 'europe',
                    color_continuous_scale=[[0, 'rgb(255,212,212)'],
                      [0.05, 'rgb(253,183,183)'],
                      [0.1, 'rgb(252,152,152)'],
                      [0.20, 'rgb(249,120,120)'],
                      [1, 'rgb(255,0,0)']])
        
        return fig
        
    # plots scatter plot depicting correlation between life expectancy and COVID mortality in each country
    def scatter_exp_mort(self):
        exp_df = life_exp()
        mortality_df = ps.execute_sql(self.conn, death_ratio())[0]
        join_df =  pd.merge(mortality_df, exp_df, left_on='COUNTRY_REGION', right_on='Country', how='inner')
        join_df.drop('COUNTRY_REGION', axis=1, inplace=True)

        fig = px.scatter(join_df, x='RATIO_DEATHS_PERC', y='Life expectancy', text='Country', 
                        title='COVID-19 Death Ratio vs. Life Expectancy')

        fig.update_traces(marker=dict(size=12, opacity=0.7, line=dict(width=2, color='DarkSlateGrey')),
                        selector=dict(mode='markers+text'))

        fig.update_layout(
            xaxis_title='Death Ratio (%)',
            yaxis_title='Life Expectancy (years)',
            showlegend=False,
            hovermode='closest',
            title_x=0.5
        )

        return fig
    
    # plots scatter plot depicting correlation between happiness score and COVID vaccination rates in each country
    def happy_vs_vaccinated(self):
        hap_df = happy_df()
        vaccines = ps.execute_sql(self.conn, countries_vacc())[0]
        join_df =  pd.merge(vaccines, hap_df, left_on='COUNTRY_REGION', right_on='Country', how='inner')

        fig = px.scatter(join_df, x='PERC_VAC', y='Happiness score', text='Country', 
                        title='Happiness VS Vaccination ratio by country')
        
        
        fig.update_traces(marker=dict(size=12, opacity=0.7, line=dict(width=2, color='DarkSlateGrey')),
                        selector=dict(mode='markers+text'))

        fig.update_layout(
            xaxis_title='% Vaccinated',
            yaxis_title='Happiness Score',
            showlegend=False,
            hovermode='closest',
            title_x=0.5
        )

        return fig


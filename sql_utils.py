import pandas as pd

"""
SQL helper queries and functions to convinient, one-line access within the main logic
"""

# Returns Life Expectancy dataset from Kaggle as dataframe
def life_exp():
    df = pd.read_csv('exp_out.csv')
    return df

# Returns Happiness Index dataset from Kaggle as dataframe
def happy_df():
    df = pd.read_csv('happy_out.csv')
    return df

# Query for extracting countries along with COVID mortality ratio
def death_ratio():
    return """
            SELECT
            D.COUNTRY_REGION,
            (SUM(J.DEATHS) / D.TOTAL_POPULATION) * 100 AS RATIO_DEATHS_PERC
        FROM
            JHU_DASHBOARD_COVID_19_GLOBAL J
        JOIN
            DATABANK_DEMOGRAPHICS D
        ON
            J.COUNTRY_REGION = D.COUNTRY_REGION
        WHERE DATE = '2023-03-10'
        GROUP BY
            D.COUNTRY_REGION,
            D.TOTAL_POPULATION
        HAVING
            RATIO_DEATHS_PERC > 0 AND RATIO_DEATHS_PERC < 100
        ORDER BY
            RATIO_DEATHS_PERC;
            """

# Query for getting 2020 infection rate data for 1 country
def country_escalation(country):
    return f"SELECT CASES, DATE FROM ECDC_GLOBAL WHERE COUNTRY_REGION = '{country}' ORDER BY DATE ASC"

# Getting one country along with vaccinates/non-vaccinated ratios
def vaccine_query(country):
    return f"""
                WITH latest_data AS ( 
                    SELECT V.COUNTRY_REGION, 
                        MAX(V.DATE) AS LATEST_DATE 
                    FROM OWID_VACCINATIONS V 
                    GROUP BY V.COUNTRY_REGION 
                )  
                
                SELECT ld.COUNTRY_REGION,  
                    (V.PEOPLE_VACCINATED / D.TOTAL_POPULATION) * 100 AS PERC_VAC, 
                    100 - ((V.PEOPLE_VACCINATED / D.TOTAL_POPULATION) * 100) AS PERC_NOT_VAC
                FROM latest_data ld
                JOIN OWID_VACCINATIONS V ON ld.COUNTRY_REGION = V.COUNTRY_REGION AND ld.LATEST_DATE = V.DATE
                JOIN DATABANK_DEMOGRAPHICS D ON ld.COUNTRY_REGION = D.COUNTRY_REGION
                WHERE PERC_VAC < 100 AND V.COUNTRY_REGION = '{country}'
                ORDER BY PERC_VAC ASC;
           """

# Getting European latest data for each country with weekly COVID cases
def european_latest():
    return """
        SELECT 
             e.COUNTRY_REGION,
             e.DATE AS MostRecentDate,
             e.CASES_WEEKLY AS MostRecentCases
    FROM ECDC_GLOBAL_WEEKLY e
    INNER JOIN (
       SELECT COUNTRY_REGION, MAX(DATE) AS MaxDate
       FROM ECDC_GLOBAL_WEEKLY
       WHERE DATE <= '2023-08-14' AND CASES_WEEKLY IS NOT NULL AND COUNTRY_REGION != 'EU/EEA (total)'
       GROUP BY COUNTRY_REGION
) subquery
ON e.COUNTRY_REGION = subquery.COUNTRY_REGION AND e.DATE = subquery.MaxDate;
        """

# Similar to vaccine_query() but for all countries and only vaccinated ratio
def countries_vacc():
    return """
            WITH latest_data AS ( 
                SELECT V.COUNTRY_REGION, 
                    MAX(V.DATE) AS LATEST_DATE 
                FROM OWID_VACCINATIONS V 
                GROUP BY V.COUNTRY_REGION 
            )  
            
            SELECT ld.COUNTRY_REGION,  
                (V.PEOPLE_VACCINATED / D.TOTAL_POPULATION) * 100 AS PERC_VAC
            FROM latest_data ld
            JOIN OWID_VACCINATIONS V ON ld.COUNTRY_REGION = V.COUNTRY_REGION AND ld.LATEST_DATE = V.DATE
            JOIN DATABANK_DEMOGRAPHICS D ON ld.COUNTRY_REGION = D.COUNTRY_REGION
            WHERE PERC_VAC < 100
            ORDER BY PERC_VAC ASC;
        """
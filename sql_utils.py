import pandas as pd

def life_exp():
    df = pd.read_csv('exp_out.csv')
    return df

def happy_df():
    df = pd.read_csv('happy_out.csv')
    return df

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


def country_escalation(country):
    return f"SELECT CASES, DATE FROM ECDC_GLOBAL WHERE COUNTRY_REGION = '{country}' ORDER BY DATE ASC"

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
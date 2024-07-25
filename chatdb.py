
import streamlit as st
import sqlite3
import pandas as pd
import google.generativeai as genai


pd.options.display.float_format = "{:,.2f}".format
pd.set_option('display.precision', 2)

st.set_page_config(layout="wide",page_title="Retrieve SQL query")

    
genai.configure(api_key="AIzaSyAEb3_JzsOkmoj4h0hdfV0JvTFn43rKyRg")

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    columns = [description[0] for description in cur.description]
    conn.commit()
    conn.close()
    return rows,columns

prompt=["""
    You are an expert in converting English questions to SQL query!
    The SQL database is about InpatientCharges with the columns such as DRG Definition, Provider Id, Provider Name
    Provider Street Address, Provider City, Provider State, Provider Zip Code, Hospital Referral Region Description,
    Total Discharges, Average Covered Charges, Average Total Payments, Average Medicare Payments;
    When writing the SQL query, ensure:
  - Column names with spaces are enclosed in square brackets [ ]
  - The SQL code should not have ``` in beginning or end
  - Do not include the word 'sql' in the output
"""]

st.title("Chat with Database")

question=st.text_input("Input: ",key="input")

submit_button = st.button(label='Ask the question')
           

st.divider()
if submit_button:
    response=get_gemini_response(question,prompt)
    st.code(response, language="sql")
    try:
        result, columns = read_sql_query(response, "inpatient_charges.db")
        
        if len(result) == 1 and len(result[0]) == 1:
            # Single value result
            st.markdown("#### Query executed successfully! Here is the result:")
            st.write(result[0][0])
        else:
            # DataFrame result
            st.markdown("#### Query executed successfully! Here are the results:")
            data = pd.DataFrame(result, columns=columns)
            st.dataframe(data)
    except Exception as e:
        st.error(f"An error occurred while executing the query: {e}")

        
        
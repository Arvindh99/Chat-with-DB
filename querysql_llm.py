# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:36:21 2024

@author: User
"""

import streamlit as st
import sqlite3
import pandas as pd
import google.generativeai as genai

data = pd.read_excel('inpatientCharges.xlsx')

conn = sqlite3.connect('inpatient_charges.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS InpatientCharges (DRG_Definition TEXT,Provider_Id INTEGER,Provider_Name TEXT,
               Provider_Street_Address TEXT, Provider_City TEXT, Provider_State TEXT, Provider_Zip_Code INTEGER,
               Hospital_Referral_Region_Description TEXT, Total_Discharges INTEGER, Average_Covered_Charges REAL,
               Average_Total_Payments REAL, Average_Medicare_Payments REAL)''')

data.to_sql('InpatientCharges', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

genai.configure(api_key="AIzaSyAEb3_JzsOkmoj4h0hdfV0JvTFn43rKyRg") # Saved in Sticky Notes

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

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

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

if submit:
    response=get_gemini_response(question,prompt)
    st.text(response)
    response=read_sql_query(response,"student.db")
    st.markdown("The Response is")
    for row in response:
        st.text(row)
import sqlite3
import pandas as pd


data = pd.read_excel('InpatientCharges_sample.xlsx')

conn = sqlite3.connect('inpatient_charges.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS InpatientCharges (DRG_Definition TEXT,Provider_Id INTEGER,Provider_Name TEXT,
               Provider_Street_Address TEXT, Provider_City TEXT, Provider_State TEXT, Provider_Zip_Code INTEGER,
               Hospital_Referral_Region_Description TEXT, Total_Discharges INTEGER, Average_Covered_Charges REAL,
               Average_Total_Payments REAL, Average_Medicare_Payments REAL)''')

data.to_sql('InpatientCharges', conn, if_exists='replace', index=False)

conn.commit()
conn.close()


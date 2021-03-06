#pip3 install pandas  This will not work without pandas!

#This file takes data from the Business_Licenses.csv (city of chicago database link below)
#https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr
#And from the Crime_data.csv (city of chicago database link below)
#https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2

import csv
import sqlite3
import pandas
import sys

firstarg=sys.argv[1]
secondarg=sys.argv[2]

conn = sqlite3.connect(":memory:")

datafile = pandas.read_csv(firstarg)
datafile.columns = [c.lower().replace(' ', '_') for c in datafile.columns]
datafile.to_sql("businesses",conn, if_exists='append',index=False)

datafile2 = pandas.read_csv("Crime_Data.csv")
datafile2.columns = [c.lower().replace(' ', '_') for c in datafile2.columns]
datafile2.to_sql("crimes",conn, if_exists='append',index=False)

conn.commit()

conn.row_factory = sqlite3.Row
b = conn.cursor()
b.execute('SELECT count(DISTINCT legal_name) as num_businesses, ward_precinct FROM businesses WHERE license_code >= 1470 and license_code <= 1477 and license_code != 1472 GROUP BY ward_precinct')
businesses = b.fetchall()

output = pandas.DataFrame(columns=['block#','#business_with_liquor','#crimes','#arrests'])
outputindx = 0
for row in businesses:
  c = conn.cursor()
  if row['ward_precinct'] != None:
    c.execute('''SELECT count(case_number) as num_crimes, count(arrest) as num_arrests FROM crimes WHERE substr(district,2,2)||CAST(ward AS TEXT) = ?''',(row['ward_precinct'].replace("-",""), ))
    crime = c.fetchone()
    outputindx += 1
    output.loc[outputindx] = [row['ward_precinct'].replace("-",""),row['num_businesses'],crime['num_crimes'],crime['num_arrests']]

conn.close()
output.to_csv("Task_9.csv")

print("Look for the Task_9.csv file in the working directory")
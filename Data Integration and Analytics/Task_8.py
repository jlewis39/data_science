#pip3 install pandas
import csv
import sqlite3
import pandas
import sys

firstarg=sys.argv[1]
conn = sqlite3.connect(":memory:")
#DOWNLOAD FOOD_INSPECTIONS from City of Chicago Data Portal!!!
datafile = pandas.read_csv(firstarg)

datafile.columns = [c.lower().replace(' ', '_') for c in datafile.columns]
datafile.to_sql("inspect",conn, if_exists='append',index=False)
conn.commit()

conn.row_factory = sqlite3.Row
inspects = conn.cursor()

inspects.execute("select *, substr(inspection_date,7,4)||substr(inspection_date,4,2)||substr(inspection_date,1,2) as date, CAST(substr(inspection_date,7,4) as integer) as year from inspect WHERE results = 'Out of Business' or results = 'Fail' ORDER BY address, date DESC")
results = inspects.fetchall()
numfailures = 0
for i,v in enumerate(results):
  yearsalive = 0
  if v['results'] == 'Out of Business':
    numfailures += 1
    flag = True
    while flag:
      i += 1
      try:
        if results[i]['address'] == v['address']:
          yearsalive = v['year'] - results[i]['year']
          print('{0}, {1}, {2}, {3}'.format(v['dba_name'],v['address'],results[i]['inspection_date'],yearsalive))
          flag = False
          break
      except IndexError:
        flag = False
print(len(results))
print(numfailures)
conn.close()
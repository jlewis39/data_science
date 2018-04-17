#pip3 install pandas  This will not work without pandas!

#This file takes data from the Business_Licenses.csv (city of chicago database link below)
#https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr
#And from the Crime_data.csv (city of chicago database link below)
#

#And then determines how many crimes take place near stores/schools/resturants based upon license type. (i.e. a resturant only counted if it selled alcohol.)
#The low leval details are that the csv files are loaded into a sqlite database stored in memory. 
import csv, sqlite3, pandas, latlongcalc
from operator import itemgetter
import sys
firstarg=sys.argv[1]
secondarg=sys.argv[2]

conn = sqlite3.connect(":memory:")
datafile = pandas.read_csv(firstarg)
datafile.columns = [c.lower().replace(' ', '_') for c in datafile.columns]
datafile.to_sql("licenses",conn, if_exists='append',index=False)
datafile2 = pandas.read_csv(secondarg)
datafile2.columns = [c.lower().replace(' ', '_') for c in datafile2.columns]
datafile2.to_sql("crimes",conn, if_exists='append',index=False)
conn.commit()

conn.row_factory = sqlite3.Row
b = conn.cursor()
b.execute('SELECT DISTINCT legal_name,address,license_code,latitude,longitude,license_term_expiration_date,substr(license_term_expiration_date,7,4) as year from licenses WHERE license_code == 1781 or license_code == 1690 or license_code == 1023 or license_code == 1584 or license_code == 1586 or license_code == 1585 or license_code == 1470 or license_code == 1474 ORDER BY address,legal_name LIMIT 500')
licenses = b.fetchall()

output = list()
for l in licenses:
  c = conn.cursor()
  c.execute('''select DISTINCT year, primary_type, arrest, description, latitude, longitude from crimes where year = ? LIMIT 500''',( l['year'], ))
  crimes = c.fetchall()
  # print(l['legal_name'],"|",l['license_description'],"|",l['latitude'],"|",l['longitude'])
  btype = 'c'
  if 1690 == l['license_code'] or 1584 == l['license_code'] or 1585 == l['license_code'] or l['license_code'] == 1586 or l['license_code'] == 1023:
    btype = 'b'
  elif 1474 == l['license_code']:
    btype = 'a'
  t_type = 0
  if 1781 == l['license_code']:
    t_type = 1
  a_type = 0
  if 1470 == l['license_code']:
    a_type = 1
  types = {}
  for c in crimes:
    onprem = 0
    if c['latitude'] != None and c['longitude'] != None and l['latitude'] != None and l['longitude'] != None:
      if latlongcalc.miles(c['latitude'],c['longitude'],l['latitude'],l['longitude']) <= 0.375:
        if latlongcalc.miles(c['latitude'],c['longitude'],l['latitude'],l['longitude']) <= 0.001:
          onprem = 1
        if str(c['year']) in types.keys():
          if c['primary_type'] in types[str(c['year'])].keys():
            tuples = types[str(c['year'])][c['primary_type']]
            types[str(c['year'])][c['primary_type']] = (tuples[0] + 1, tuples[1] + c['arrest'], tuples[2] + onprem)
          else:
            types[str(c['year'])][c['primary_type']] = (1,c['arrest'],onprem)
        else:
          types[str(c['year'])] = {}
          types[str(c['year'])][c['primary_type']]= (1,c['arrest'],onprem)
  if types:
    for key in types:
      for key2 in types[key]:
        print('{0},{1},"{2}","{3}",{4},{5},{6},{7},{8},{9}'.format(key,btype,l['legal_name'],l['address'],t_type,a_type,key2,types[key][key2][0],types[key][key2][1],types[key][key2][2]) )
conn.close()
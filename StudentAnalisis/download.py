"""
	script downloads data from SQL server and stores it in download.txt line by line,
	also converts:
		null  -> None
		true  -> True
		false -> False
"""

import pymssql
import codecs
import time

IP = '161.53.18.12:1955'
username = 'roko'
password = 'g546z6rhtf'
DBname='ExperientialSamplingAnalyticsDev'

conn = pymssql.connect(server=IP, user=username, password=password, database=DBname) 
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))

cursor = conn.cursor()  

# CONVERT(NVARCHAR(MAX), LogEvent.JSONparams) -> otherwise you need to decode string to windows-1252
query = '''
SELECT [User].Name, LogEvent.Id, LogEvent.EventName, LogEvent.EventType, LogEvent.Time, CONVERT(NVARCHAR(MAX), LogEvent.JSONparams), LogEvent.ContextualInfoId FROM LogEvent 
JOIN ContextualInfo ON LogEvent.ContextualInfoId = ContextualInfo.Id
JOIN [User] ON ContextualInfo.UserId = [User].Id
WHERE JSONparams LIKE '{"lesson":%isCollaborative%' AND eventName = 'widget_log' 
AND ( 
	(ContextualInfo.Time BETWEEN '12/01/2016' and '12/01/2016 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '12/09/2016' and '12/09/2016 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '01/18/2017' and '01/18/2017 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '01/19/2017' and '01/19/2017 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '02/22/2017' and '02/22/2017 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '03/24/2017' and '03/24/2017 23:59:59') 
)
'''
print("executing query ({})".format(query))
cursor.execute(query)
print("query executed") 

i = 0
start_time = time.time()
with codecs.open('download.txt', 'w', "utf-8-sig") as f:
	for row in cursor:	
		i += 1
		if time.time() - start_time > 10: 
			start_time = time.time()
			print("i", i)
			
		row = str(row).replace('null', 'None').replace('true', 'True').replace('false', 'False').replace('Ć', 'C').replace('Č', 'C').replace('Ð', 'Đ')
		#gore navedena Đ i Đ nisu ista!!!!!!!!!!
		
		f.write("{}\n".format(row))
		
print("i", i)
print('closing connection')
conn.close() 
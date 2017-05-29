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
DBname='ExperientialSamplingAnalyticsDev2'

conn = pymssql.connect(server=IP, user=username, password=password, database=DBname) 
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))

cursor = conn.cursor()  

# CONVERT(NVARCHAR(MAX), LogEvent.JSONparams) -> otherwise you need to decode string to windows-1252
query = '''  
	SELECT [User].Name, LogEvent.Id, LogEvent.EventName, LogEvent.EventType, LogEvent.Time, CONVERT(NVARCHAR(MAX), LogEvent.JSONparams), LogEvent.ContextualInfoId FROM LogEvent 
	JOIN ContextualInfo ON LogEvent.ContextualInfoId = ContextualInfo.Id
	JOIN [User] ON ContextualInfo.UserId = [User].Id
	WHERE JSONparams LIKE '%{%}%' AND LogEvent.EventType = 'Player' and LogEvent.EventName = 'widget_log' AND
	JSONparams NOT LIKE '%waitingForChecker%' AND JSONparams NOT LIKE '%confirmSolution%' AND JSONparams NOT LIKE '%needToDiscuss%'  
'''

print("executing query ({})".format(query))
cursor.execute(query)
print("query executed") 

i = 0
start_time = time.time()
with codecs.open('download_player.txt', 'w', "utf-8-sig") as f:
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
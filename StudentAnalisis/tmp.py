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

query = '''
SELECT TOP 1 [User].Name, CONVERT(NVARCHAR(MAX), LogEvent.JSONparams) FROM LogEvent 
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
AND [User].Name = 'MARKO KNEŽEVIĆ'
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
		
		
		print(str(row))	
		row = str(row).replace('null', 'None').replace('true', 'True').replace('false', 'False')
		
		f.write("{}\n".format(row))
		
print("i", i)
print('closing connection')
conn.close() 
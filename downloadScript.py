import pymssql
import codecs

IP = '161.53.18.12:1955'
username = 'roko'
password = 'g546z6rhtf'
DBname='ExperientialSamplingAnalyticsDev'

conn = pymssql.connect(server=IP, user=username, password=password, database=DBname) 
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))

cursor = conn.cursor()  

query = '''
SELECT LogEvent.* FROM LogEvent 
JOIN ContextualInfo ON LogEvent.ContextualInfoId = ContextualInfo.Id
WHERE JSONparams like '{"lesson":"%' AND ( 
	(ContextualInfo.Time BETWEEN '12/01/2016' and '12/01/2016 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '12/09/2016' and '12/09/2016 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '01/18/2017' and '01/18/2017 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '01/19/2017' and '01/19/2017 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '02/22/2017' and '02/22/2017 23:59:59') OR 
	(ContextualInfo.Time BETWEEN '03/24/2017' and '03/24/2017 23:59:59') 
)'''
print("executing query ({})".format(query))
cursor.execute(query)

i = 0
print("query executed") 
with codecs.open('logs_lession.txt', 'w', "utf-8-sig") as f:
	for row in cursor:
		f.write("{}\n".format(row))
		if i % 1000 == 0: print("line '{}' has been written. ({})".format(str(row).encode("utf-8"), i))
		i += 1
		
print("i", i)
print('closing connection')
conn.close() 
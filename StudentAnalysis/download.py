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
import argparse
import os
from utils import get_file_name_from_dates, get_value_from_file, type_constraint
from datetime import datetime

parser = argparse.ArgumentParser(description="Downloads logs from specified dates for specified type.")
parser.add_argument('type', help="lesson type. Allowed types: collaborative, competitive, AR", type=str)
parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')

parser.add_argument('-ip', help="IP address of the database", default="161.53.18.12", type=str)
parser.add_argument('-port', help="PORT of the database", default=1955, type=int)
parser.add_argument('-db', help="Database name", default="ExperientialSampling1", type=str)
					
args = parser.parse_args()

IP = args.ip+":"+str(args.port)
username = get_value_from_file('config.txt', 'username')
password = get_value_from_file('config.txt', 'password')
DBname=args.db

file_type ={
	"collaborative" : "download_collaborative",
	"AR" : "download_AR",
	"competitive" : "download_player"
}

file_name = get_file_name_from_dates(file_type[args.type], args.date)
if os.path.isfile(file_name): 
	print("file with name {} already exists".format(file_name))
	exit(1)

conn = pymssql.connect(server=IP, user=username, password=password, database=DBname) 
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))

cursor = conn.cursor()  

def generate_query(dates, type):
	query = '''
	SELECT [User].Id, [User].Name, LogEvent.Id, LogEvent.EventName, LogEvent.EventType, LogEvent.Time, CONVERT(NVARCHAR(MAX), LogEvent.JSONparams), LogEvent.ContextualInfoId FROM LogEvent 
	JOIN ContextualInfo ON LogEvent.ContextualInfoId = ContextualInfo.Id
	JOIN [User] ON ContextualInfo.UserId = [User].Id
	WHERE {} 
	AND ( 
		{}
	)
	'''.format(
		type_constraint[type],
		" OR\n\t\t".join(["(ContextualInfo.Time BETWEEN '{0}/{1}/{2}' and '{0}/{1}/{2} 23:59:59')".format(date.month, date.day, date.year) for date in dates]))
	
	return query
		

query = generate_query(args.date, args.type)
print("executing query ({})".format(query))

cursor.execute(query)
print("query executed") 

i = 0
start_time = time.time()
print("writing to {}".format(file_name))
with codecs.open(file_name, 'w', "utf-8-sig") as f:
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







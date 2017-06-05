import pymssql
import codecs
import argparse
import time
from datetime import datetime

from utils import get_file_name_from_dates

allowed_types = ["competitive", "collaborative", "AR"]
type_constraint = {
	"collaborative": '''JSONparams LIKE '{"lesson":%isCollaborative%' AND eventName = 'widget_log' ''',
	#"competitive": '''JSONparams LIKE '%{%}%' AND LogEvent.EventType = 'Player' AND LogEvent.EventName = 'widget_log' AND JSONparams NOT LIKE '%waitingForChecker%' AND JSONparams NOT LIKE '%confirmSolution%' AND JSONparams NOT LIKE '%needToDiscuss%'  ''',
	"competitive": '''JSONparams LIKE '%{%}%' AND LogEvent.EventType = 'Player' AND LogEvent.EventName = 'widget_log' ''',
	"AR": '''JSONparams LIKE '%{%}%' AND LogEvent.EventType LIKE 'AR%' '''
}

parser = argparse.ArgumentParser(description="Gets relevant dates for types of lessons.")
parser.add_argument('-types', help="types of lessons", default=allowed_types, type=str, nargs='*')

parser.add_argument('-sd', help="Starting date (dd.mm.YYYY)", default=datetime(1990, 1, 1), type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs="?")
parser.add_argument('-ed', help="Ending date (dd.mm.YYYY)", default=datetime.now(), type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs="?")

parser.add_argument('-ip', help="IP address of the database", default="161.53.18.12", type=str)
parser.add_argument('-port', help="PORT of the database", default=1955, type=int)
parser.add_argument('-db', help="Database name", default="ExperientialSamplingAnalyticsDev2", type=str)
					
args = parser.parse_args()

IP = args.ip+":"+str(args.port)
username = 'roko'
password = 'g546z6rhtf'
DBname=args.db

if any(type not in allowed_types for type in args.types):
	print("allowed types: {}".format(allowed_types))
	exit()

conn = pymssql.connect(server=IP, user=username, password=password, database=DBname)
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))

cursor = conn.cursor()

def generate_query(type, starting_date, ending_date):	
	query = '''
	SELECT DISTINCT CONVERT(VARCHAR(11),ContextualInfo.[Time],104) FROM LogEvent
	JOIN ContextualInfo ON LogEvent.ContextualInfoId = ContextualInfo.Id
	WHERE 
	{} 
	AND (ContextualInfo.Time BETWEEN '{}/{}/{}' and '{}/{}/{} 23:59:59')
	'''.format(type_constraint[type], starting_date.month, starting_date.day, starting_date.year, ending_date.month, ending_date.day, ending_date.year)
	
	return query
	

for type in args.types:	
	query = generate_query(type, args.sd, args.ed)

	print("executing query ({})".format(query))
	cursor.execute(query)
	print("query executed") 

	i = 0
	start_time = time.time()
	file_name = get_file_name_from_dates('dates_{}'.format(type), [args.sd, args.ed])
	print("writing to {}".format('dates_{}.txt'.format(type)))
	with codecs.open(file_name, 'w', "utf-8-sig") as f:
		for row in cursor:	
			i += 1
			if time.time() - start_time > 10: 
				start_time = time.time()
				print("i", i)
			
			f.write("{}\n".format(row[0]))
		
		print("i", i)
		
		print("finished writing to {}".format('dates_{}.txt'.format(type)))
	
	

print('closing connection')
conn.close() 
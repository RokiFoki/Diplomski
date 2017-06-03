import os
import argparse
from utils import get_file_name_from_dates, execute_python_script
from datetime import datetime
import time
import codecs

# -------------------- parsing arguments ---------------------------------- #
parser = argparse.ArgumentParser(description="Executes pipeline.")
parser.add_argument('type', help="types of lessons", type=str)

parser.add_argument('sd', help="Starting date (dd.mm.YYYY)", default=datetime(1990, 1, 1), type=lambda x: datetime.strptime(x, '%d.%m.%Y'))
parser.add_argument('ed', help="Ending date (dd.mm.YYYY)", default=datetime.now(), type=lambda x: datetime.strptime(x, '%d.%m.%Y'))

parser.add_argument('-ip', help="IP address of the database", default="161.53.18.12", type=str)
parser.add_argument('-port', help="PORT of the database", default=1955, type=int)
parser.add_argument('-db', help="Database name", default="ExperientialSamplingAnalyticsDev2", type=str)

action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-t', help='calculate lessons/users (train system)', type=int)
action.add_argument('-e', help='evaluate users\' score', action='store_true')
					
args = parser.parse_args()

# get all dates in range	
execute_python_script("get_dates.py", ["-types", args.type, "-sd", args.sd.strftime("%d.%m.%Y"), "-ed", args.ed.strftime("%d.%m.%Y"), "-ip", args.ip, "-port", args.port, "-db", args.db])

dates_file_name = get_file_name_from_dates("dates_{}".format(args.type), [args.sd, args.ed])
if not os.path.isfile(get_file_name_from_dates("dates_{}".format(args.type), [args.sd, args.ed])):
	print("ERROR: get_dates.py didn't create {}".format(dates_file_name))
	exit()

download_file = {
	"AR": "download_AR.py", 
	"competitive": "download_player.py",
	"collaborative": "download.py"
}

preprocess = {
	"AR": "quotes_AR.py", 
	"competitive": "slashes_quotes_filter_player.py",
	"collaborative": "slashes_qoutes_commas.py"
}
	
analyse_users = {
	"AR": "analyseUsers_AR.py",
	"competitive": "analyseUsers_player.py",
	"collaborative": "analyseUsers.py",
}
	
with codecs.open(get_file_name_from_dates("dates_{}".format(args.type), [args.sd, args.ed]), "r", "utf-8-sig") as fin:
	if args.e:
		for date in fin:
			date = date.strip()
			
			execute_python_script(download_file[args.type], [date, "-ip", args.ip, "-port", args.port, "-db", args.db])
			execute_python_script(preprocess[args.type], [date])
			execute_python_script(analyse_users[args.type], [date, "-d", "lessons.txt", "-r", get_file_name_from_dates("users", [datetime.strptime(date, "%d.%m.%Y")])])
		
		time.sleep(3)
	else:
		dates = " ".join([date.strip() for date in fin.readlines()])
		print(dates)
		execute_python_script(download_file[args.type], [dates, "-ip", args.ip, "-port", args.port, "-db", args.db])
		execute_python_script(preprocess[args.type], [dates])
		
		execute_python_script(analyse_users[args.type], [dates, "-d", "lessons.txt", "-r", get_file_name_from_dates("users", [datetime.strptime(date, "%d.%m.%Y") for date in dates.split(" ")])])
	
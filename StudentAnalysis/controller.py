import os
import argparse
from utils import get_file_name_from_dates, execute_python_script
from datetime import datetime
import time
import codecs

# -------------------- parsing arguments ---------------------------------- #
parser = argparse.ArgumentParser(description="Controller script that is used for downloading, filtering and training system / evaulating users.")
parser.add_argument('type', help="type of lessons. Allowed types: collaborative, competitive, AR", type=str)

parser.add_argument('starting_date', help="Starting date (dd.mm.YYYY)", default=datetime(1990, 1, 1), type=lambda x: datetime.strptime(x, '%d.%m.%Y'))
parser.add_argument('ending_date', help="Ending date (dd.mm.YYYY)", default=datetime.now(), type=lambda x: datetime.strptime(x, '%d.%m.%Y'))
parser.add_argument('-f', help="Take first F elements", type=int)

parser.add_argument('-ip', help="IP address of the database", default="161.53.18.12", type=str)
parser.add_argument('-port', help="PORT of the database", default=1955, type=int)
parser.add_argument('-db', help="Database name", default="ExperientialSampling1", type=str)

action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-t', help='calculate lessons/users (train system)', type=int)
action.add_argument('-e', help='evaluate users\' score', action='store_true')
					
args = parser.parse_args()

# get all dates in range	
arguments = ["-types", args.type, "-sd", args.starting_date.strftime("%d.%m.%Y"), "-ed", args.ending_date.strftime("%d.%m.%Y"), "-ip", args.ip, "-port", args.port, "-db", args.db]
if args.f: arguments += ["-f", args.f]

execute_python_script("get_dates.py", arguments)

dates_file_name = get_file_name_from_dates("dates_{}".format(args.type), [args.starting_date, args.ending_date])
if not os.path.isfile(get_file_name_from_dates("dates_{}".format(args.type), [args.starting_date, args.ending_date])):
	print("ERROR: get_dates.py didn't create {}".format(dates_file_name))
	exit(1)

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

analyse_lessons = {
	"AR": "analyseLessons_AR.py",
	"competitive": "analyseLessons_player.py",
	"collaborative": "analyseLessons.py",
}

type_tag = {
	"collaborative": "collaborative",
	"AR": "AR",
	"competitive": "player"
}
	
with codecs.open(get_file_name_from_dates("dates_{}".format(args.type), [args.starting_date, args.ending_date]), "r", "utf-8-sig") as fin:
	if args.e:
		dates_lines = fin.readlines()
		for date in dates_lines:
			date = date.strip()
			
			execute_python_script("download.py", [args.type, date, "-ip", args.ip, "-port", args.port, "-db", args.db])
			execute_python_script(preprocess[args.type], [date])
			execute_python_script(analyse_users[args.type], [date, "-d", "lessons", "-r", 
				get_file_name_from_dates("users", [datetime.strptime(date, "%d.%m.%Y")], suffix="")])
		
		dates = " ".join([date.strip() for date in dates_lines])
		execute_python_script("preprocess_predict.py", [args.type, dates])
	else:
		dates = " ".join([date.strip() for date in fin.readlines()])
		execute_python_script("download.py", [args.type, dates, "-ip", args.ip, "-port", args.port, "-db", args.db])
		execute_python_script(preprocess[args.type], [dates])
		
		for i in range(args.t): #lessons.txt, lessons_AR.txt, lessons_player.txt
			print("iteration {}".format(i+1))
			execute_python_script(analyse_users[args.type], [dates, "-i", "img{}".format(i), "-d", "lessons", "-r", "users"])
			execute_python_script(analyse_lessons[args.type], [dates, "-i", "img{}".format(i), "-d", "users", "-r", "lessons"])
				
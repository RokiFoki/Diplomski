""" TIP: you may want to use controller.py """

import os 
import sys
import time
import argparse

from utils import get_file_name_from_dates, execute_python_script

arser = argparse.ArgumentParser(description="Controller script that is used for downloading filtering and training system / evaulating users.")
parser.add_argument('type', help="type of lessons", type=str)
parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')

parser.add_argument('-n', help="number of iterations", type=int)

args = parser.parse_args()
n = args.n
dates = args.date

print("running {} iterations".format(n))

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

for i in range(n):
	print("iteration {} started".format(i+1))
	execute_python_script(analyse_users[args.type], [dates, "-i", "img{}".format(i), "-d", "lessons", "-r", "users"])
	execute_python_script(analyse_lessons[args.type], [dates, "-i", "img{}".format(i), "-d", "users", "-r", "lessons"])
import os
import argparse
from utils import get_file_name_from_dates, execute_python_script
from datetime import datetime
import time
import codecs
import glob
from shutil import copyfile


parser = argparse.ArgumentParser(description="")
parser.add_argument('type', help="types of lessons", type=str)
parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
					
args = parser.parse_args()
dates = args.date
type = args.type

for file_name in glob.glob('tmp/users/logs/a/*_real.txt'):
	new_file_name = "{}_tmp.txt".format(file_name[:-9])
	copyfile(file_name, new_file_name)

for date in dates:
	file = get_file_name_from_dates("users", [date], prefix="tmp/users/logs/", suffix="_{}.txt".format(type))
	
	if os.path.isfile(file):
		with codecs.open(file, "r", "utf-8-sig") as flog:
			print("reading file {}".format(file))
			for line in flog:
				user, grade = line.strip().split(":")
				
				with open("tmp/users/results/{}_{}_tmp.txt".format(user, type), "a") as fuser:
					fuser.write("{}:{}\n".format(date.strftime("%d.%m.%Y"), grade))
	

	
for file_name in glob.glob('tmp/users/results/*_tmp.txt'):
	new_file_name = "{}_real.txt".format(file_name[:-8])	
	d = {}
	
	with open(file_name, "r") as f:
		for line in f:
			date, grade = line.strip().split(":")
			d[date] = grade
	
	with open(new_file_name, "w") as f:
		dates = sorted([datetime.strptime(date, "%d.%m.%Y") for date in d.keys()])
		
		for date in dates:
			date_str = date.strftime("%d.%m.%Y")
			f.write("{}:{}\n".format(date_str, d[date_str]))
			
	os.remove(file_name)
		
import os
import argparse
from utils import get_file_name_from_dates, execute_python_script
from datetime import datetime
import time
import codecs
import glob
from shutil import copyfile


parser = argparse.ArgumentParser(description="script that extracts students data from date stored data")
parser.add_argument('type', help="type of lessons. Allowed types: collaborative, competitive, AR", type=str)
parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
					
args = parser.parse_args()
dates = args.date
type = args.type

type_tag = {
	"collaborative": "",
	"AR": "_AR",
	"competitive": "_player"
}

users = set()

print("copying _real files")
for file_name in glob.glob('tmp/users/results/*_real.txt'):
	new_file_name = "{}_tmp.txt".format(file_name[:-9])
	copyfile(file_name, new_file_name)

i = 0
print("copying _real files to _tmp files")
for date in dates:
	file = get_file_name_from_dates("users", [date], prefix="tmp/users/logs/", suffix="{}.txt".format(type_tag[type]))

	if os.path.isfile(file):
		with codecs.open(file, "r", "utf-8-sig") as flog:
			for line in flog:
				user, grade = line.strip().split(":")
				
				with open("tmp/users/results/{}{}_tmp.txt".format(user, type_tag[type]), "a") as fuser:
					fuser.write("{}:{}\n".format(date.strftime("%d.%m.%Y"), grade))

				users.add(user)

				i += 1
	
print("finished ({} changes)".format(i))

i = 0
print("create _real files")
for file_name in glob.glob('tmp/users/results/*_tmp.txt'):
	new_file_name = "{}_real.txt".format(file_name[:-8])	
	d = {}
	
	with open(file_name, "r") as f:
		for line in f:
			date, grade = line.strip().split(":")
			
			d[date] = max(float(d.get(date, 0)), float(grade))
	
	with open(new_file_name, "w") as f:
		student_dates = sorted([datetime.strptime(date, "%d.%m.%Y") for date in d.keys()])
		
		for date in student_dates:
			date_str = date.strftime("%d.%m.%Y")
			f.write("{}:{}\n".format(date_str, d[date_str]))

	i += 1
			
	os.remove(file_name)

print("finished ({} changes)".format(i))

with codecs.open(get_file_name_from_dates('users', dates), 'w', "utf-8-sig") as f:
	for user in users:
		f.write("{}\n".format(user.strip()))